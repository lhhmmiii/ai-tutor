import os
import sys
from typing import Any, Optional, List, Dict, Union

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
from llama_index.core import StorageContext
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
    """A class for handling document-based question answering using vector storage and retrieval.
    
    This class provides functionality for:
    - Creating and managing vector indices for documents
    - Adding documents to indices
    - Querying documents using natural language
    - Managing document metadata and references
    - Updating and deleting documents
    
    The class uses LlamaIndex for vector storage and retrieval, with support for:
    - HTML, Office, and Table file formats
    - Chat-based interactions with memory
    - Metadata filtering for user-specific queries
    - Batch processing of documents
    """
    
    def __init__(self, user_id: str = '', db_name: str = 'AI-Tutor', user_collection: str = 'users',\
                 storage_context: Optional[StorageContext] = None) -> None:
        """Initialize the DocumentQA service.
        
        Args:
            user_id: The ID of the user
            user_collection: The user collection for storing user data
            storage_context: The storage context for vector indices
        """
        self.user = User(db_name = db_name, collection_name = user_collection)
        self.user_id = user_id
        self.storage_context = storage_context
        self.html_file = HtmlFile()
        self.table_file = TableFile()
        self.office_file = OfficeFile()
        self.chat_memory = ChatMemory(user_id=user_id)


    def create_index_without_document(self) -> VectorStoreIndex:
        """Create new index without nodes.

        This method initializes a new VectorStoreIndex without any documents,
        using the provided storage context.

        Args:
            None

        Returns:
            VectorStoreIndex: A new, empty vector index.

        Raises:
            HTTPException: If there's an error creating the index.
        """
        try:
            index_struct = IndexDict()
            index = VectorStoreIndex(
                index_struct=index_struct,
                storage_context=self.storage_context,
                show_progress=True,
            )
            return index
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating index: {str(e)}")

    async def create_index_with_document(self, file: Any, url: Optional[str] = None, is_header: bool = False) -> VectorStoreIndex:
        """Create new index with nodes from a document.

        This method creates a new VectorStoreIndex with nodes extracted from
        the provided document file or URL.

        Args:
            file: The document file to process.
            url: The URL of the document to process (if file is not provided).
            is_header: Boolean indicating whether to include headers in processing.

        Returns:
            VectorStoreIndex: A new vector index containing the document's nodes.

        Raises:
            HTTPException: If there's an error processing the document or creating the index.
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
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating index with document: {str(e)}")

    async def add_nodes_to_index(
        self,
        index: VectorStoreIndex,
        file: Any,
        url: Optional[str],
        is_header: bool,
        embed_model: BaseEmbedding,
        insert_batch_size: int = 2048,
        show_progress: bool = True,
        **insert_kwargs: Any,
    ) -> None:
        """Add document nodes to an existing index.
        
        This method processes a document (from file or URL), splits it into nodes,
        generates embeddings for each node, and adds them to the vector store and
        document store. It also updates the index structure and user's document list.
        
        Args:
            index: The index to add nodes to
            file: Uploaded file containing the document
            url: URL to fetch document from (if file not provided)
            is_header: Whether to include headers in document processing
            embed_model: Model to use for generating embeddings
            insert_batch_size: Number of nodes to process in each batch
            show_progress: Whether to show progress during embedding generation
            **insert_kwargs: Additional arguments to pass to vector store add method

        Raises:
            HTTPException: If there's an error processing the document or adding nodes to the index.
        """
        try:
            index_struct = index.index_struct
            vector_store = index.storage_context.vector_store
            docstore = index.storage_context.docstore
            index_store = index.storage_context.index_store
            
            # Load and process document
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
            
            # Process nodes in batches
            for nodes_batch in iter_batch(nodes, insert_batch_size):
                # Generate embeddings for batch
                nodes_batch = get_node_with_embedding(
                    nodes_batch, embed_model, show_progress
                )
                new_ids = vector_store.add(nodes_batch, **insert_kwargs)

                # Add nodes to stores
                for node, new_id in zip(nodes_batch, new_ids, strict=False):
                    # Remove embedding to avoid duplication
                    node_without_embedding = node.model_copy()
                    node_without_embedding.embedding = None

                    # Update stores
                    index_struct.add_node(node_without_embedding, text_id=new_id)
                    docstore.add_documents([node_without_embedding], allow_update=True)
                    index_store.add_index_struct(index_struct)
            
            # Update user's document list
            ref_doc_ids = self.get_ref_doc_ids_from_node_ids(index.index_id, index)
            self.user.update_document_list(
                user_id=self.user_id,
                file_name=file.filename,
                index_id=index.index_id,
                ref_doc_ids=ref_doc_ids,
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error adding nodes to index: {str(e)}")

    def get_nodes(self, index: VectorStoreIndex) -> List[Any]:
        """Retrieve all nodes from the given index.

        This method fetches all nodes stored in the document store of the provided index.

        Args:
            index: The index containing the nodes to retrieve.

        Returns:
            list: A list of all nodes in the index.

        Raises:
            HTTPException: If there's an error retrieving the nodes.
        """
        try:
            node_ids = list(index.index_struct.nodes_dict.values())
            nodes = index.docstore.get_nodes(node_ids)
            return nodes
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving nodes: {str(e)}")

    def get_nodes_by_ref_doc_id(self, index: VectorStoreIndex, ref_doc_id: str) -> List[Any]:
        """Get all nodes associated with a specific reference document ID.
        
        This method retrieves nodes from the document store that are linked to the given
        reference document ID. It performs the following steps:
        1. Gets the node IDs associated with the reference document
        2. Validates that the node IDs exist in the current index structure
        3. Retrieves and returns the actual nodes from the document store
        
        Args:
            index: The index containing the document store to search
            ref_doc_id: The reference document ID to find nodes for
            
        Returns:
            list: The nodes associated with the reference document ID
            
        Raises:
            HTTPException: If there is an error retrieving the nodes
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
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving nodes by reference document ID: {str(e)}")

    def query(self, index: VectorStoreIndex, query_str: str) -> Any:
        """Process a user query and generate a response using the document index.

        This method performs the following steps:
        1. Applies metadata filters to restrict the search to the current user's documents.
        2. Sets up a vector index retriever to find relevant documents.
        3. Configures node postprocessors to refine the retrieved results.
        4. Initializes a context-aware chat engine with the retriever, chat memory, and postprocessors.
        5. Generates and returns a response to the user's query.

        Args:
            index: The document index to search.
            query_str (str): The user's query string.

        Returns:
            The chat engine's response to the query.

        Raises:
            HTTPException: If an error occurs during the query process.
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
                retriever=retriever,
                memory=chat_memory,
                node_postprocessors=node_postprocessors,
            )
            response = chat_engine.chat(query_str)
            return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

    def query_by_ref_doc_id(self, index: VectorStoreIndex, ref_doc_id: str, query_str: str) -> Dict[str, Any]:
        """Query documents by reference document ID.

        This method retrieves and queries documents based on the provided reference
        document ID. It filters the documents using metadata, retrieves relevant
        nodes using a vector store, and processes the query using a retriever query engine.

        Args:
            index: The index object to query.
            ref_doc_id (str): The reference document ID to filter by.
            query_str (str): The query string to process.

        Returns:
            dict: A dictionary containing the response to the query.

        Raises:
            HTTPException: If there is an error during the query process.
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
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error querying by reference document ID: {str(e)}")

    def query_by_index_id_and_ref_doc_id(
        self, index: VectorStoreIndex, index_id: str, ref_doc_id: str, query_str: str
    ) -> Dict[str, Any]:
        """Query documents by index ID and reference document ID.

        This method retrieves and queries documents based on the provided index ID
        and reference document ID. It filters the documents using metadata, retrieves
        relevant nodes using a vector store, and processes the query using a retriever
        query engine.

        Args:
            index: The index object to query.
            index_id (str): The ID of the index to query.
            ref_doc_id (str): The reference document ID to filter by.
            query_str (str): The query string to process.

        Returns:
            dict: A dictionary containing the response to the query.

        Raises:
            HTTPException: If there is an error during the query process.
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
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error querying by index ID and reference document ID: {str(e)}")

    def update_document(self, index: VectorStoreIndex, file: Any, url: Optional[str], is_header: bool, embed_model: BaseEmbedding) -> None:
        """Update a document in the index by replacing its content.
        
        This method updates a document by:
        1. Loading and processing the new document file/URL
        2. Deleting the old document's nodes from the index using its ref_doc_id
        3. Adding the new document's nodes to the index
        
        Args:
            index: The index containing the document to update
            file: The new document file to replace the old content
            url: URL to fetch new document from (if file not provided)
            is_header: Whether to include headers when processing the new document
            embed_model: Model to use for generating embeddings for new nodes
            
        Raises:
            HTTPException: If there is an error during the update process
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
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating document: {str(e)}")

    def delete_indexes(self, index: VectorStoreIndex) -> None:
        """Delete all indexes and their associated data from storage.
        
        This method performs a complete deletion of all indexes and their data by:
        1. Retrieving all index structures from storage
        2. Collecting their index IDs
        3. Iteratively deleting each index using delete_index_by_index_id
        
        Args:
            index: The index containing the storage context to delete from
            
        Raises:
            HTTPException: If there is an error during deletion
        """
        try:
            index_structs = index.storage_context.index_store.index_structs()
            list_index_id = []
            for index_struct in index_structs:
                list_index_id.append(index_struct.index_id)
            for index_id in list_index_id:
                self.delete_index_by_index_id(index, index_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting indexes: {str(e)}")

    def delete_index_by_index_id(self, index: VectorStoreIndex, index_id: str) -> None:
        """Delete an index and all its associated data from storage.
        
        This method performs a complete deletion of an index and all its associated data:
        1. Removes the index from the user's document list
        2. Retrieves all node IDs associated with the index
        3. Deletes the index structure from the index store
        4. Removes all documents from the document store
        5. Deletes all vector data from the vector store
        
        Args:
            index: The index to delete
            index_id: The ID of the index to delete
            
        Raises:
            HTTPException: If there is an error during deletion
        """
        try:
            # Remove index from user's document list
            self.user.delete_document_list(index_id=index_id, ref_doc_ids=None)
            
            # Get all node IDs associated with this index
            node_ids = list(
                index.storage_context.index_store.get_index_struct(
                    index_id
                ).nodes_dict.values()
            )
            
            # Delete index structure
            index.storage_context.index_store.delete_index_struct(index_id)
            
            # Delete all associated documents
            for node_id in node_ids:
                index.docstore.delete_document(node_id)
                
            # Delete vector data
            index.vector_store.delete_nodes(node_ids)
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting index by index ID: {str(e)}")

    def delete_index_by_ref_doc_id(self, index: VectorStoreIndex, index_id: str, ref_doc_id: str) -> None:
        """Delete a reference document and its associated nodes from the index.
        
        This method removes a specific reference document and all its associated nodes from the index.
        It handles cleanup across multiple storage components:
        1. Removes the document from the user's document list
        2. Deletes associated nodes from the index structure
        3. Removes the index structure if it becomes empty
        4. Deletes the reference document from the document store
        5. Removes the document's data from the vector store
        
        Args:
            index: The index containing the reference document
            index_id: The ID of the index
            ref_doc_id: The ID of the reference document to delete
            
        Raises:
            HTTPException: If there is an error during deletion
        """
        try:
            # Remove document from user's document list
            self.user.delete_document_list(index_id=index_id, ref_doc_ids=[ref_doc_id])
            
            # Remove nodes from index structure
            ref_doc_info = index.docstore.get_ref_doc_info(ref_doc_id)
            if ref_doc_info is not None:
                for node_id in ref_doc_info.node_ids:
                    index.index_struct.delete(node_id)
                    
            # Handle empty index structure
            if index.index_struct.nodes_dict == {}:
                index_id = index.index_id
                index.storage_context.index_store.delete_index_struct(index_id)
            else:
                index.storage_context.index_store.add_index_struct(index.index_struct)
                
            # Remove document from stores
            index.docstore.delete_ref_doc(ref_doc_id)
            index.vector_store.delete(ref_doc_id)
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting index by reference document ID: {str(e)}")

    def load_index_by_index_id(self, index_id: Optional[str] = None) -> VectorStoreIndex:
        """Load an index from storage by its ID.
        
        This method loads a vector index from the storage context. If no index_id is provided,
        it loads the first available index. Otherwise, it loads the specific index requested.
        
        Args:
            index_id (str, optional): The ID of the index to load. If None, loads first available index.
            
        Returns:
            VectorStoreIndex: The loaded index instance
            
        Raises:
            HTTPException: If there is an error loading the index
        """
        try:
            if index_id is None:
                indices = load_indices_from_storage(self.storage_context)
                return indices[0]
            else:
                index = load_index_from_storage(self.storage_context, index_id=index_id)
            return index
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error loading index by index ID: {str(e)}")

    def get_ref_doc_ids_from_node_ids(self, index_id: str, index: VectorStoreIndex) -> List[str]:
        """Get reference document IDs associated with nodes in an index.
        
        This method retrieves all reference document IDs that are associated with
        the nodes in a given index. It does this by checking which reference documents
        contain nodes that are present in the index's node dictionary.
        
        Args:
            index_id (str): The ID of the index to check
            index (VectorStoreIndex): The index instance containing the nodes
            
        Returns:
            list: List of reference document IDs associated with the index's nodes
        """
        index_struct = index.storage_context.index_store.get_index_struct(index_id)
        node_ids = list(index_struct.nodes_dict.values())
        ref_doc_ids = []
        for key, value in index.docstore.get_all_ref_doc_info().items():
            if value.node_ids[0] in node_ids:
                ref_doc_ids.append(key)
        return ref_doc_ids

    def create_query_engine_tool(self, index: VectorStoreIndex) -> QueryEngineTool:
        """Create a query engine tool for document-based question answering.
        
        This method creates a QueryEngineTool instance that can be used to answer
        questions based on the documents in the index. The tool is configured to
        only provide answers from the indexed documents.
        
        Args:
            index (VectorStoreIndex): The index to create the query engine from
            
        Returns:
            QueryEngineTool: A tool configured for document-based question answering
        """
        query_engine = index.as_query_engine()
        query_engine_tool = QueryEngineTool.from_defaults(
            query_engine=query_engine,
            name='DocumentQA',
            description='Only answer the question from the documents'
        )
        return query_engine_tool
