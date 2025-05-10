from pymongo import MongoClient
from pymongo.operations import SearchIndexModel
from dotenv import load_dotenv
import os

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")


def connect_to_mongo(db_name: str, collection_name):
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]
    return collection

def create_vector_search_index(mongo_uri: str = mongo_uri, db_name: str = 'StudyEnglishData', collection_name: str = 'Grammar'):
    mongo_client = MongoClient(mongo_uri)
    collection = mongo_client[db_name][collection_name]

    search_index_model = SearchIndexModel(
        definition={
            "fields": [
                {
                    "type": "vector",
                    "path": "embedding",
                    "numDimensions": 1024,
                    "similarity": "cosine"
                },
                {
                    "type": "filter",
                    "path": "metadata.user_id"
                }
            ]
        },
        name="vector_index",
        type="vectorSearch"
    )

    collection.create_search_index(model=search_index_model)
    print("✅ Search index 'vector_index' created successfully.")