from pydantic import BaseModel
from typing import List

class GrammarIssue(BaseModel):
    original: str
    corrected: str
    explanation: str

    class Config:
        json_schema_extra = {
            "example": {
                "original": "She go to the store.",
                "corrected": "She goes to the store.",
                "explanation": "Subject-verb agreement error."
            }
        }

class GrammarCheckResult(BaseModel):
    corrected_text: str
    issues_found: List[GrammarIssue]

    class Config:
        json_schema_extra = {
            "example": {
                "corrected_text": "She goes to the store.",
                "issues_found": [
                    {
                        "original": "She go to the store.",
                        "corrected": "She goes to the store.",
                        "explanation": "Subject-verb agreement error."
                    }
                ]
            }
        }