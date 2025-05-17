from pydantic import BaseModel, Field


class LevelAnalysis(BaseModel):
    level: str = Field(..., description="Estimated CEFR level (e.g., A1, B2, C1).")
    score: float = Field(..., ge=0, le=100, description="Confidence score (0-100).")

    class Config:
        json_schema_extra = {
            "example": {
                "level": "B2",
                "score": 85.0,
            }
        }