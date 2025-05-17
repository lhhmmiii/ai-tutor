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

class RoleplayParams(BaseModel):
    topic: str  
    context: str  
    ai_role: str  

    class Config:
        json_schema_extra = {
            "example": {
                "topic": "coffee",
                "context": "at a coffee shop",
                "ai_role": "barista",
            }
        }