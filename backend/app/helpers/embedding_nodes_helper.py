from collections.abc import Sequence

from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.schema import BaseNode, MetadataMode


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
