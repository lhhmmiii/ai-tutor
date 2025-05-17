from pydantic import BaseModel
from typing import Optional

class WritingFeedback(BaseModel):
    coherence_and_structure: str
    vocabulary_use: str
    clarity_and_conciseness: str
    tone_and_purpose: str
    overall_comment: Optional[str] = None 

    class Config:
        json_schema_extra = {
            "example": {
                "coherence_and_structure": "The essay has a clear structure with a strong introduction, body, and conclusion.",
                "vocabulary_use": "The vocabulary is appropriate for the target audience and context.",
                "clarity_and_conciseness": "The writing is clear and concise, with no unnecessary jargon.",
                "tone_and_purpose": "The tone is formal and appropriate for an academic essay.",
                "overall_comment": "Overall, this is a well-written essay that meets the assignment requirements."
            }
        }