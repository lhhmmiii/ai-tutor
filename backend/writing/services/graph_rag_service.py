import os
import sys
from datetime import datetime
from llama_index.core import Document
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from writing.utils.format_time_utils import _format_file_timestamp
from writing.utils.file_utils import load_file
from writing.config import embed_model, setting
from writing.config.llm import gemini
from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore
from llama_index.core import PropertyGraphIndex
from llama_index.core.indices.property_graph import SchemaLLMPathExtractor
import nest_asyncio

nest_asyncio.apply()

embed_model = embed_model()
setting(llm=gemini, embed_model=embed_model)

grammar_data_path = "writing/data/Adjectives_and_prepositions.txt"



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
with open(grammar_data_path, "r", encoding="utf-8") as f:
    text = f.read()
doc = create_docs(text, "test")
documents.append(doc)

# Note: used to be `Neo4jPGStore`
graph_store = Neo4jPropertyGraphStore(
    username="neo4j",
    password="mega-harvard-shrink-april-fire-3407",
    url="bolt://127.0.0.1:7687",
)

print(00000000000000000000)
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
print(444444444444444444444444444)
retriever = index.as_retriever(
    include_text=False,  # include source text in returned nodes, default True
)

print(11111111111111111111)
nodes = retriever.retrieve("When use 'a' and 'an'")

print(22222222222222222222)
for node in nodes:
    print(node.text)

query_engine = index.as_query_engine(include_text=True)

response = query_engine.query("When use 'a' and 'an'")

print(str(response))