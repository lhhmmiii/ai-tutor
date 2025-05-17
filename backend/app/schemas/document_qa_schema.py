from typing import Any
from pydantic import BaseModel, Field

class Index(BaseModel):
    index_id: str = Field(description="Index store identity")
    nodes_dict: dict = Field(
        default_factory=dict, description="Dictionary of node_ids in index store"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "index_id": "2bb458e1-1d37-42fe-98ef-e65b89a7a62d",
                "nodes_dict": {
                    "7566e72c-db57-4419-8226-21ce8101ae3b": "7566e72c-db57-4419-8226"
                    "-21ce8101ae3b"
                },
            }
        }


class QueryResponse(BaseModel):
    response: str = Field(description="Index store identity")
    source_nodes: list[Any] = Field(
        default_factory=list, description="Dictionary of node_ids in index store"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "response": "Le Huu Hung",
                "source_nodes": [
                    {
                        "id": "1e1a1acb-babf-4f2c-9bbd-159aeeabc74e",
                        "text": "Le Huu Hung hoc lop 21TNT1",
                        "metadata": {
                            "total_pages": 1,
                            "creation_date": "2025-01-03T09:40:13Z",
                            "file_name": "example.txt",
                            "user_id": "67765d192ed0f67dbf0adac7",
                            "source": 1,
                        },
                    }
                ],
            }
        }


class QueryRequest(BaseModel):
    query_str: str = Field(description="Query from user")
    user_id: str = Field(description="User identity")
    ref_doc_id: str = Field(
        description="Reference document identity", default_factory=""
    )
    index_id: str = Field(description="Index identity", default_factory="")

    class Config:
        json_schema_extra = {
            "example": {
                "query_str": "What is COT?",
                "user_id": "7848945894578dhjfhjdfda",
                "ref_doc_id": "38978941",
                "index_id": "745678459",
            }
        }

class DocQADeleteResponse(BaseModel):
    content: str = Field(description="message for user")

    class Config:
        json_schema_extra = {"example": {"content": "Delete successful"}}