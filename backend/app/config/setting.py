import os

from llama_index.core.settings import Settings
from llama_index.embeddings.cohere import CohereEmbedding



def setting(llm, embed_model):
    """Configure global settings for LLM and embedding model in LLamaIndex.
    
    Args:
        embed_model: The embedding model to be used for text embeddings
    """
    # Settings
    Settings.llm = llm
    Settings.embed_model = embed_model

def embed_model():
    """Initialize and return a Cohere embedding model.
    
    Returns:
        CohereEmbedding: Configured embedding model instance using Cohere's API
    """
    embed_model = CohereEmbedding(
        api_key=os.environ["COHERE_API_KEY"],
        model_name="embed-english-v3.0",
        input_type="search_query",
    )
    return embed_model
