from pydantic import BaseModel, Field


class TextExtractor(BaseModel):
    id: str = Field(max_length=100, description="Document identity")
    text: str = Field(description="document content")
    metadata: dict = Field(default_factory=dict, description="Document metadata")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "21tnt1",
                "text": "Le Huu Hung",
                "metadata": {
                    "total_pages": 1,
                    "creation_date": "2025-01-03T09:14:12Z",
                    "file_name": "example.txt",
                    "user_id": "67763c8fc8fb066c663ddc48",
                    "source": 1,
                },
            }
        }
