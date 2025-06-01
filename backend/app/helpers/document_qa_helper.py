from collections.abc import Sequence
from typing import Optional
from llama_index.core import StorageContext
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.schema import BaseNode, MetadataMode
from llama_index.core import (
    VectorStoreIndex,
    load_index_from_storage,
    load_indices_from_storage,
)
from llama_index.core.tools.query_engine import QueryEngineTool


def embed_nodes(
    nodes: Sequence[BaseNode], embed_model: BaseEmbedding, show_progress: bool = False
) -> dict[str, list[float]]:
    """Get embeddings of the given nodes, run embedding model if necessary.

    Args:
        nodes (Sequence[BaseNode]): The nodes to embed.
        embed_model (BaseEmbedding): The embedding model to use.
        show_progress (bool): Whether to show progress bar.

    Returns:
        Dict[str, List[float]]: A map from node id to embedding.
    """
    id_to_embed_map: dict[str, list[float]] = {}

    texts_to_embed = []
    ids_to_embed = []
    for node in nodes:
        if node.embedding is None:
            ids_to_embed.append(node.node_id)
            texts_to_embed.append(node.get_content(metadata_mode=MetadataMode.EMBED))
        else:
            id_to_embed_map[node.node_id] = node.embedding

    new_embeddings = embed_model.get_text_embedding_batch(
        texts_to_embed, show_progress=show_progress
    )

    for new_id, text_embedding in zip(ids_to_embed, new_embeddings, strict=False):
        id_to_embed_map[new_id] = text_embedding

    return id_to_embed_map


def get_node_with_embedding(
    nodes: Sequence[BaseNode], embed_model: BaseEmbedding, show_progress: bool = False
) -> list[BaseNode]:
    """
    Get tuples of id, node, and embedding.

    Allows us to store these nodes in a vector store.
    Embeddings are called in batches.

    """
    id_to_embed_map = embed_nodes(nodes, embed_model, show_progress=show_progress)

    results = []
    for node in nodes:
        embedding = id_to_embed_map[node.node_id]
        result = node.model_copy()
        result.embedding = embedding
        results.append(result)
    return results

def load_index_by_index_id(storage_context, index_id: Optional[str] = None) -> VectorStoreIndex:
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
    if index_id is None:
        indices = load_indices_from_storage(storage_context)
        return indices[0]
    else:
        index = load_index_from_storage(storage_context, index_id=index_id)
    return index

def create_query_engine_tool(self, index: VectorStoreIndex, name: str, description: str) -> QueryEngineTool:
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
        name=name, 
        description=description
    )
    return query_engine_tool