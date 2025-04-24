from pydantic import BaseModel
from typing import Optional

class WritingFeedback(BaseModel):
    coherence_and_structure: str
    vocabulary_use: str
    clarity_and_conciseness: str
    tone_and_purpose: str
    overall_comment: Optional[str] = None 