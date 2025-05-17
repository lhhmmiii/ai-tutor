from llama_index.core import QueryBundle
from llama_index.core.postprocessor import LLMRerank, SimilarityPostprocessor
from llama_index.core.schema import NodeWithScore


class SimilarityPostprocessorWithAtLeastOneResult(SimilarityPostprocessor):
    """Similarity-based Node processor. Return always one result if result is empty"""

    @classmethod
    def class_name(cls) -> str:
        return "SimilarityPostprocessorWithAtLeastOneResult"

    def _postprocess_nodes(
        self, nodes: list[NodeWithScore], query_bundle: QueryBundle | None = None
    ) -> list[NodeWithScore]:
        """Postprocess nodes."""
        # Call parent class's _postprocess_nodes method first
        new_nodes = super()._postprocess_nodes(nodes, query_bundle)

        if not new_nodes:  # If the result is empty
            return [max(nodes, key=lambda x: x.score)] if nodes else []

        return new_nodes


def create_node_postprocessor(similarity_cutoff, top_n, choice_batch_size):
    node_postprocessors = [
        SimilarityPostprocessorWithAtLeastOneResult(
            similarity_cutoff=similarity_cutoff
        ),
        LLMRerank(top_n=top_n, choice_batch_size=choice_batch_size),
    ]
    return node_postprocessors
