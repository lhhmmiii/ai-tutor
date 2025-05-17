from typing import List
from pydantic import BaseModel


class VocabularyEntry(BaseModel):
    word: str                         # Từ hoặc cụm từ tiếng Anh
    meaning_vn: str                   # Nghĩa tiếng Việt (theo ngữ cảnh nếu có)
    sample_sentence: str             # Một câu ví dụ
    synonyms: List[str]              # Danh sách từ đồng nghĩa (nếu có)
    image_idea: str                  # Gợi ý hình ảnh để ghi nhớ
    additional_examples: List[str]   # 4 câu ví dụ bổ sung

    class Config:
        json_schema_extra = {
            "example": {
                "word": "interested in",
                "meaning_vn": "quan tâm tới",
                "sample_sentence": "I'm interested in improving my cooking skills.",
                "synonyms": ["fascinated by", "curious about"],
                "image_idea": "A person attentively reading a book about Korean culture.",
                "additional_examples": [
                    "He's interested in working abroad.",
                    "They're interested in environmental issues.",
                    "Are you interested in joining our club?",
                    "I'm very interested in classical music."
                ]
                }
        }

class VocabularyResponse(BaseModel):
    word_id: str
    vocabulary: VocabularyEntry

    class Config:
        json_schema_extra = {
            "example": {
                "word_id": "123",
                "vocabulary": VocabularyEntry.Config.json_schema_extra["example"]
            }
        }

class VocabularyUpdateRequest(BaseModel):
    word: str
    meaning_vn: str | None = None
    sample_sentence: str | None = None
    synonyms: List[str] | None = None
    image_idea: str | None = None
    additional_examples: List[str] | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "word": "interested in",
                "meaning_vn": "quan tâm tới",
                "sample_sentence": "I'm interested in improving my cooking skills.",
                "synonyms": ["fascinated by", "curious about"],
                "image_idea": "A person attentively reading a book about Korean culture.",
                "additional_examples": [
                    "He's interested in working abroad.",
                    "They're interested in environmental issues.",
                    "Are you interested in joining our club?",
                    "I'm very interested in classical music."
                ]
                }
        }
