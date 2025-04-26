from fastapi import APIRouter
from writing.services.vocabulary_support_service import VocabularySupportService
from writing.schemas.vocabulary_support_schema import VocabularyEntry

vocabulary_support_router = APIRouter(tags=["vocabulary_support"])
vocabulary_support_service = VocabularySupportService()

@vocabulary_support_router.post("/vocabulary")
async def vocabulary_support(text: str) -> VocabularyEntry:
    """
    Generate the meaning, sentence example, synonym(if any), prompt which is used to generate images
    """
    

    # Call the grammar check service and return the result
    result = vocabulary_support_service.generate(text)
    return result