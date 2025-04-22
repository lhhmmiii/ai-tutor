from pydantic import BaseModel
from typing import List

class GrammarIssue(BaseModel):
    original: str
    corrected: str
    explanation: str

class GrammarCheckResult(BaseModel):
    corrected_text: str
    issues_found: List[GrammarIssue]