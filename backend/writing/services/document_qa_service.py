import os
import sys
from typing import Any

from fastapi import HTTPException
from llama_index.core import (
    VectorStoreIndex,
    load_index_from_storage,
    load_indices_from_storage,
)
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.chat_engine import ContextChatEngine
from llama_index.core.data_structs.data_structs import IndexDict
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.tools.query_engine import QueryEngineTool
from llama_index.core.utils import iter_batch
from llama_index.core.vector_stores import (
    ExactMatchFilter,
    FilterOperator,
    MetadataFilters,
)

from writing.services.base_service import BaseQA
from writing.services.chat_memory_service import ChatMemory
from writing.services.extract_html_file_service import HtmlFile
from writing.services.extract_office_file_service import OfficeFile
from writing.services.extract_table_file_service import TableFile
from writing.services.user_service import User
from writing.helpers.embedding_nodes_helper import get_node_with_embedding
from writing.helpers.post_process_nodes_helper import create_node_postprocessor
from writing.utils.file_utils import load_file


class DocumentQA(BaseQA):
    def __init__(self, user_id, user_collection, storage_context):
        self.user = User(user_collection)
        self.user_id = user_id
        self.storage_context = storage_context
        self.html_file = HtmlFile()
        self.table_file = TableFile()
        self.office_file = OfficeFile()
        self.chat_memory = ChatMemory(user_id = user_id)


    def create_index_without_document(self):
        """Create new index without nodes
        Args:
        db_name: Database name
        collection_name: Collection name
        """
        try:
            index_struct = IndexDict()
            index = VectorStoreIndex(
                index_struct=index_struct,
                storage_context=self.storage_context,
                show_progress=True,
            )
            return index
        except HTTPException as e:
            raise e

    async def create_index_with_document(self, file, url, is_header):
        """Create new index with nodes
        Args:
            db_name: Database name
            collection_name: Collection name
            path: file or directory path
        """
        try:
            # Initative
            docs = await load_file(
                html_file=self.html_file,
                table_file=self.table_file,
                office_file=self.office_file,
                file=file,
                user_id = self.user_id,
                url=url,
                is_header=is_header,
            )
            nodes = SentenceSplitter().get_nodes_from_documents(docs)
            self.storage_context.docstore.add_documents(nodes)
            # Set vector.stores_text = False(If I don't do so, index_store
            # don't have node_ids)
            self.storage_context.vector_store.stores_text = False
            index = VectorStoreIndex(
                nodes, storage_context=self.storage_context, show_progress=True
            )  # Generating embeding from docstore
            self.storage_context.vector_store.stores_text = True
            ref_doc_ids = self.get_ref_doc_ids_from_node_ids(index.index_id, index)
            # Update User DB
            self.user.update_document_list(
                self.user_id, file.filename, index.index_id, ref_doc_ids
            )
            return index
        except HTTPException as e:
            raise e

    async def add_nodes_to_index(
        self,
        index,
        file,
        url,
        is_header,
        embed_model: BaseEmbedding,
        insert_batch_size: int = 2048,
        show_progress: bool = True,
        **insert_kwargs: Any,
    ) -> None:
        try:
            """Add document to index."""
            index_struct = index.index_struct
            vector_store = index.storage_context.vector_store
            docstore = index.storage_context.docstore
            index_store = index.storage_context.index_store
            docs = await load_file(
                html_file=self.html_file,
                table_file=self.table_file,
                office_file=self.office_file,
                file=file,
                user_id=self.user_id,
                url=url,
                is_header=is_header,
            )
            nodes = SentenceSplitter().get_nodes_from_documents(docs)
            for nodes_batch in iter_batch(nodes, insert_batch_size):
                nodes_batch = get_node_with_embedding(
                    nodes_batch, embed_model, show_progress
                )
                new_ids = vector_store.add(nodes_batch, **insert_kwargs)

                for node, new_id in zip(nodes_batch, new_ids, strict=False):
                    # NOTE: remove embedding from node to avoid duplication
                    node_without_embedding = node.model_copy()
                    node_without_embedding.embedding = None

                    index_struct.add_node(node_without_embedding, text_id=new_id)
                    docstore.add_documents([node_without_embedding], allow_update=True)
                    index_store.add_index_struct(index_struct)
            # Update User DB
            ref_doc_ids = self.get_ref_doc_ids_from_node_ids(index.index_id, index)
            self.user.update_document_list(
                user_id=self.user_id,
                file_name=file.filename,
                index_id=index.index_id,
                ref_doc_ids=ref_doc_ids,
            )
        except HTTPException as e:
            raise e

    def get_nodes(self, index):
        try:
            node_ids = list(index.index_struct.nodes_dict.values())
            nodes = index.docstore.get_nodes(node_ids)
            return nodes
        except HTTPException as e:
            raise e

    def get_nodes_by_ref_doc_id(self, index, ref_doc_id):
        """Get docstore by ref_doc_id
        Args:
          ref_doc_id
        """
        try:
            node_ids_in_ref_doc = index.docstore.get_ref_doc_info(ref_doc_id).node_ids
            node_ids = list(index.index_struct.nodes_dict.values())
            if node_ids_in_ref_doc is None:
                pass
            elif node_ids_in_ref_doc[0] not in node_ids:
                node_ids_in_ref_doc = []
            nodes = index.docstore.get_nodes(node_ids_in_ref_doc)
            return nodes
        except HTTPException as e:
            raise e

    def query(self, index, query_str):
        """Response answer from user query
        Args:
          query_str: user query
        """
        try:
            metadata_filters = MetadataFilters(
                filters=[ExactMatchFilter(key="user_id", value=self.user_id)]
            )
            retriever = VectorIndexRetriever(
                index=index, filters=metadata_filters, similarity_top_k=5
            )
            node_postprocessors = create_node_postprocessor(
                similarity_cutoff=0.82, top_n=3, choice_batch_size=10
            )
            chat_memory = self.chat_memory.chat_memory
            chat_engine = ContextChatEngine.from_defaults(
                retriever = retriever,
                memory = chat_memory,
                node_postprocessors = node_postprocessors,
            )
            response = chat_engine.chat(query_str)
            return response
        except HTTPException as e:
            raise e

    def query_by_ref_doc_id(self, index, ref_doc_id, query_str):
        """Response answer from user query
        Args:
          ref_doc_id: referece document id
          query_str: user query
        """
        try:
            metadata_filters = MetadataFilters(
                filters=[
                    ExactMatchFilter(key="user_id", value=self.user_id),
                    ExactMatchFilter(key="ref_doc_id", value=ref_doc_id),
                ]
            )
            vector_store_retriever = VectorIndexRetriever(
                index=index, filters=metadata_filters, similarity_top_k=5
            )
            node_postprocessors = create_node_postprocessor(
                similarity_cutoff=0.82, top_n=3, choice_batch_size=10
            )
            query_engine = RetrieverQueryEngine(
                retriever=vector_store_retriever,
                node_postprocessors=node_postprocessors,
            )
            response = query_engine.query(query_str)
            return {"response": response.response}
        except HTTPException as e:
            raise e

    def query_by_index_id_and_ref_doc_id(
        self, index, index_id, ref_doc_id, query_str
    ):
        """Response answer from user query
        Args:
          index_id: index id
          ref_doc_id: referece document id
          query_str: user query
        """
        try:
            ref_doc_ids = self.get_ref_doc_ids_from_node_ids(index_id, index)
            metadata_filters = MetadataFilters(
                filters=[
                    ExactMatchFilter(key="user_id", value=self.user_id),
                    ExactMatchFilter(
                        key="ref_doc_id", operator=FilterOperator.IN, value=ref_doc_ids
                    ),
                    ExactMatchFilter(key="ref_doc_id", value=ref_doc_id),
                ]
            )
            vector_store_retriever = VectorIndexRetriever(
                index=index, filters=metadata_filters, similarity_top_k=5
            )
            node_postprocessors = create_node_postprocessor(
                similarity_cutoff=0.82, top_n=3, choice_batch_size=10
            )
            query_engine = RetrieverQueryEngine(
                retriever=vector_store_retriever,
                node_postprocessors=node_postprocessors,
            )
            response = query_engine.query(query_str)
            return {"response": response.response}
        except HTTPException as e:
            raise e

    def update_document(self, index, file, url, is_header, embed_model):
        """Update content by ref_doc_id
        Args:
            new_document
        """
        try:
            documents = load_file(
                html_file=self.html_file,
                table_file=self.table_file,
                office_file=self.office_file,
                file=file,
                user_id=self.user_id,
                url=url,
                is_header=is_header,
            )
            ref_doc_id = documents.get_doc_id()
            self.delete_index_by_ref_doc_id(index, ref_doc_id)
            self.add_nodes_to_index(
                index=index,
                file=file,
                user_id=self.user_id,
                url=url,
                is_header=is_header,
                embed_model=embed_model,
            )
        except HTTPException as e:
            raise e

    def delete_indexes(self, index):
        try:
            index_structs = index.storage_context.index_store.index_structs()
            list_index_id = []
            for index_struct in index_structs:
                list_index_id.append(index_struct.index_id)
            for index_id in list_index_id:
                self.delete_index_by_index_id(index, index_id)
        except HTTPException as e:
            raise e

    def delete_index_by_index_id(self, index, index_id):
        """Delete index_store by index_id
        Args:
          index_id
        """
        try:
            # Delete User DB
            self.user.delete_document_list(index_id=index_id, ref_doc_ids=None)
            #
            node_ids = list(
                index.storage_context.index_store.get_index_struct(
                    index_id
                ).nodes_dict.values()
            )  # node_ids in index_id
            # Delete index_struct
            index.storage_context.index_store.delete_index_struct(index_id)
            # Delete documents
            for node_id in node_ids:
                index.docstore.delete_document(node_id)
            # delete data in vector store
            index.vector_store.delete_nodes(node_ids)
        except HTTPException as e:
            raise e

    def delete_index_by_ref_doc_id(self, index, index_id, ref_doc_id):
        """Delete docstore by ref_doc_id
        Args:
          ref_doc_id
        """
        try:
            # Delete User DB
            self.user.delete_document_list(index_id=index_id, ref_doc_ids=[ref_doc_id])
            # Delete node_ids in index_struct
            ref_doc_info = index.docstore.get_ref_doc_info(ref_doc_id)
            if ref_doc_info is not None:
                for node_id in ref_doc_info.node_ids:
                    index.index_struct.delete(node_id)
            if index.index_struct.nodes_dict == {}:
                index_id = index.index_id
                index.storage_context.index_store.delete_index_struct(index_id)
            else:
                index.storage_context.index_store.add_index_struct(index.index_struct)
            # Delete documents in ref_doc_id
            index.docstore.delete_ref_doc(ref_doc_id)
            # delete data in vector store
            index.vector_store.delete(ref_doc_id)
        except HTTPException as e:
            raise e

    def load_index_by_index_id(self, index_id=None):
        if index_id is None:
            indices = load_indices_from_storage(self.storage_context)
            return indices[0]
        else:
            index = load_index_from_storage(self.storage_context, index_id=index_id)
        return index

    def get_ref_doc_ids_from_node_ids(self, index_id, index):
        index_struct = index.storage_context.index_store.get_index_struct(index_id)
        node_ids = list(index_struct.nodes_dict.values())
        ref_doc_ids = []
        for key, value in index.docstore.get_all_ref_doc_info().items():
            if value.node_ids[0] in node_ids:
                ref_doc_ids.append(key)
        return ref_doc_ids

    def create_query_engine_tool(self, index):
        query_engine = index.as_query_engine()
        query_engine_tool = QueryEngineTool.from_defaults(query_engine=query_engine,
                            name = 'DocumentQA',description = 'Only answer the question\
                                                                from the documents')
        return query_engine_tool

