from typing import List, Optional
from pydantic import BaseModel


class VocabularyEntry(BaseModel):
    word: str                         # Từ hoặc cụm từ tiếng Anh
    meaning_vn: str                   # Nghĩa tiếng Việt (theo ngữ cảnh nếu có)
    sample_sentences: List[str]      # Một câu ví dụ
    synonyms: List[str]              # Danh sách từ đồng nghĩa (nếu có)
    pronunciation: str               # Phát âm của từ hoặc cụm từ

    class Config:
        json_schema_extra = {
            "example": {
                "word": "interested in",
                "meaning_vn": "quan tâm tới",
                "sample_sentences": ["I'm interested in improving my cooking skills.", "He's interested in working abroad.", "They're interested in environmental issues.", "Are you interested in joining our club?", "I'm very interested in classical music."],
                "synonyms": ["fascinated by", "curious about"],
                "pronunciation": "/ˈɪn.trə.stɪd ɪn/"
            }
        }

class VocabularyResponse(BaseModel):
    word_id: str
    image_url: Optional[str] = None
    vocabulary: VocabularyEntry

    class Config:
        json_schema_extra = {
            "example": {
                "word_id": "123",
                "image_url": "https://example.com/image.jpg",
                "vocabulary": VocabularyEntry.Config.json_schema_extra["example"]
            }
        }

class VocabularyUpdateRequest(BaseModel):
    word: str
    meaning_vn: Optional[str] = None
    sample_sentences: Optional[List[str]] = None
    synonyms: Optional[List[str]] = None
    pronunciation: Optional[str] = None
    image_url: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "word": "interested in",
                "meaning_vn": "quan tâm tới",
                "sample_sentences": ["I'm interested in improving my cooking skills.", "He's interested in working abroad.", "They're interested in environmental issues.", "Are you interested in joining our club?", "I'm very interested in classical music."],
                "synonyms": ["fascinated by", "curious about"],
                "pronunciation": "/ˈɪn.trə.stɪd ɪn/",
                "image_url": "https://example.com/image.jpg",
                }
        }
