import os
from pymongo import MongoClient
from fastapi import Request
import qdrant_client
from dotenv import load_dotenv

from llama_index.core import StorageContext
from llama_index.graph_stores.neo4j import Neo4jGraphStore
from llama_index.storage.docstore.mongodb import MongoDocumentStore
from llama_index.storage.index_store.mongodb import MongoIndexStore
from llama_index.vector_stores.qdrant import QdrantVectorStore
from app.services.document_qa_service import DocumentQA
from app.services.user_service import User




# load variables from .env file
load_dotenv()


def initialize_storage_context(db_name, collection_name):
    """Initialize and configure the storage context for document indexing and retrieval.
    
    This function sets up three main components:
    1. MongoDB-based index store for storing index structures
    2. MongoDB-based document store for storing document nodes
    3. Qdrant vector store for storing and retrieving embeddings
    
    Args:
        db_name (str): Name of the MongoDB database to use
        collection_name (str): Name of the Qdrant collection for vector storage
        
    Returns:
        StorageContext: Configured storage context instance with all components initialized
    """
    mongo_uri = os.getenv("MONGO_URI")
    qdrant_url = os.getenv("QDRANT_URI")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    
    # Initialize MongoDB-based index store
    index_store = MongoIndexStore.from_uri(uri=mongo_uri, db_name=db_name)
    
    # Initialize MongoDB-based document store
    docstore = MongoDocumentStore.from_uri(uri=mongo_uri, db_name=db_name)
    
    # Initialize Qdrant vector store
    client = qdrant_client.QdrantClient(
        url=qdrant_url, 
        api_key=qdrant_api_key, 
        timeout=30, 
        https=True
    )
    vector_store = QdrantVectorStore(client=client, collection_name=collection_name)
    
    # # Graph Store
    # graph_store = Neo4jGraphStore(
    #     username="neo4j",
    #     password= os.getenv("NEO4J_PASSWORD"),
    #     url=os.getenv("NEO4J_URI"),
    #     database="neo4j"
    # )

    # Create and return storage context with all components
    storage_context = StorageContext.from_defaults(
        docstore=docstore,
        index_store=index_store,
        vector_store=vector_store,
        # graph_store=graph_store
    )
    return storage_context



def get_llm(request: Request):
    """Get the LLM instance from the application state.
    
    Args:
        request (Request): FastAPI request object containing application state
        
    Returns:
        The LLM instance stored in the application state
    """
    return request.app.state.llm

def get_embed_model(request: Request):
    """Get the embedding model instance from the application state.
    
    Args:
        request (Request): FastAPI request object containing application state
        
    Returns:
        The embedding model instance stored in the application state
    """
    return request.app.state.embed_model


def get_index_instance(user_id, request: Request):
    """Get a DocumentQA instance from the application state.
    
    This function creates and returns a DocumentQA instance configured with the user's
    collection and storage context from the application state.
    
    Args:
        user_id: The ID of the user to create the instance for
        request (Request): FastAPI request object containing application state
        
    Returns:
        DocumentQA: Configured DocumentQA instance for document question answering
    """
    app_state = request.app.state
    return DocumentQA(
        storage_context=app_state.storage_context,
        user_id = user_id
    )


