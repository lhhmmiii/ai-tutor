import os
import sys
from datetime import datetime
from llama_index.core import Document
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from writing.utils.format_time_utils import _format_file_timestamp
from writing.utils.file_utils import load_file
from writing.config import embed_model
from writing.config.llm import gemini
from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore
from llama_index.core import PropertyGraphIndex
from llama_index.core.indices.property_graph import SchemaLLMPathExtractor


embed_model = embed_model()

grammar_data_path = "writing\data"

def create_docs(texts: str = '', file_name: str = ''):
    metadata = {}
    metadata["total_length"] = len(texts)
    metadata["creation_date"] = _format_file_timestamp(
        timestamp=datetime.now().timestamp(), include_time=True
    )
    metadata["file_name"] = str(file_name)
    doc = Document(text=text, extra_info=metadata)
    return doc

documents = []
file_names = os.listdir(grammar_data_path)
for file_name in file_names:
    with open(os.path.join(grammar_data_path, file_name), "r") as f:
        text = f.read()
    doc = load_file(text, file_name)
    documents.append(doc)

# Note: used to be `Neo4jPGStore`
graph_store = Neo4jPropertyGraphStore(
    username="neo4j",
    password="mega-harvard-shrink-april-fire-3407",
    url="bolt://127.0.0.1:7687",
)


index = PropertyGraphIndex.from_documents(
    documents,
    embed_model=embed_model,
    kg_extractors=[
        SchemaLLMPathExtractor(
            llm=gemini
        )
    ],
    property_graph_store=graph_store,
    show_progress=True,
)

retriever = index.as_retriever(
    include_text=False,  # include source text in returned nodes, default True
)

nodes = retriever.retrieve("When use 'a' and 'an'")

for node in nodes:
    print(node.text)