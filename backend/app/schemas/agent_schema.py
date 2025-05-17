from pydantic import BaseModel

class WritingAgentRequest(BaseModel):
    user_id: str
    question: str 

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "124",
                "question": "1234555",
            }
        }
