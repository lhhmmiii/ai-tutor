from fastapi import APIRouter, Depends
from writing.services.vocabulary_support_service import VocabularySupportService
from writing.schemas.vocabulary_support_schema import VocabularyEntry, VocabularyResponse, VocabularyUpdateRequest
from typing import List
from writing.helpers.jwt_token_helper import validate_token

vocabulary_support_router = APIRouter(tags=["vocabulary_support"])
vocabulary_support_service = VocabularySupportService(db_name = "AI-Tutor", collection_name = "vocabularies")


@vocabulary_support_router.post("/vocabulary", dependencies = [Depends(validate_token)])
async def add_word(user_id: str, text: str) -> VocabularyResponse:
    """
    Generate the meaning, sentence example, synonym(if any), prompt which is used to generate images
    """
    # Call the grammar check service and return the result
    result = vocabulary_support_service.add_word(user_id, text)
    return result

@vocabulary_support_router.get("/vocabulary", dependencies = [Depends(validate_token)])
async def get_word(word_id: str) -> VocabularyResponse:
    """
    Get a vocabulary entry by user_id and word_id.
    """
    result = vocabulary_support_service.get_word(word_id)
    result = VocabularyResponse(word_id = word_id, vocabulary = result)
    return result

@vocabulary_support_router.get("/vocabularies", dependencies = [Depends(validate_token)])
async def get_words(user_id: str) -> List[VocabularyResponse]:
    """
    Get all vocabulary entries for a user.
    """
    results = []
    word_ids, responses = vocabulary_support_service.get_words(user_id)
    for word_id, result in zip(word_ids, responses):
        results.append(VocabularyResponse(word_id = word_id, vocabulary = result))
    return results

@vocabulary_support_router.put("/vocabulary", dependencies = [Depends(validate_token)])
async def update_word(word_id: str, updates: VocabularyUpdateRequest = None) -> str:
    """
    Update fields of a vocabulary entry for a user.
    """
    message = vocabulary_support_service.update_word(word_id, updates)
    return message

@vocabulary_support_router.delete("/vocabulary", dependencies = [Depends(validate_token)])
async def delete_word(word_id: str) -> str:
    """
    Delete a vocabulary entry by user_id and word_id.
    """
    if vocabulary_support_service.delete_word(word_id):
        return "Delete successfully"


