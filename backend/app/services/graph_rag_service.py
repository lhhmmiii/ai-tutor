import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from datetime import datetime
from llama_index.core import Document
from app.utils.format_time_utils import _format_file_timestamp
from app.utils.file_utils import load_file
from app.config import embed_model, setting
from app.config.llm import gemini
from llama_index.core.indices.property_graph import SchemaLLMPathExtractor
from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore
from llama_index.core import PropertyGraphIndex
from llama_index.core import KnowledgeGraphIndex
from llama_index.core import SimpleDirectoryReader
import nest_asyncio
from dotenv import load_dotenv

load_dotenv()

nest_asyncio.apply()

KnowledgeGraphIndex.from_documents()

def initialize_settings():
    global embed_model
    embed_model = embed_model()
    setting(llm=gemini, embed_model=embed_model)

def create_docs(text: str = '', file_name: str = ''):
    metadata = {
        "total_length": len(text),
        "creation_date": _format_file_timestamp(
            timestamp=datetime.now().timestamp(), include_time=True
        ),
        "file_name": str(file_name)
    }
    doc = Document(text=text, extra_info=metadata)
    return doc

def load_documents_from_path(path: str):
    documents = []
    for file in os.listdir(path):
        with open(os.path.join(path, file), "r", encoding="utf-8") as f:
            text = f.read()
        doc = create_docs(text, file)
        documents.append(doc)
    return documents

def create_graph_store():
    return Neo4jPropertyGraphStore(
        username="neo4j",
        password=os.getenv("NEO4J_PASSWORD"),
        url=os.getenv("NEO4J_URL"),
    )

def create_index(documents, graph_store):
    return PropertyGraphIndex.from_documents(
        documents,
        embed_model=embed_model,
        kg_extractors=[SchemaLLMPathExtractor(llm=gemini)],
        property_graph_store=graph_store,
        show_progress=True,
    )

def retrieve_nodes(index, query: str):
    retriever = index.as_retriever(include_text=False)
    nodes = retriever.retrieve(query)
    for node in nodes:
        print(node.text)

def query_index(index, query: str):
    query_engine = index.as_query_engine(include_text=True)
    response = query_engine.query(query)
    print(str(response))

def main():
    initialize_settings()
    # documents = load_documents_from_path("writing/data/preprocessed")
    documents = SimpleDirectoryReader("writing/data/paul_graham/").load_data()
    graph_store = create_graph_store()
    index = create_index(documents, graph_store)
    retrieve_nodes(index, "When use 'a' and 'an'")
    query_index(index, "When use 'a' and 'an'")

if __name__ == "__main__":
    main()