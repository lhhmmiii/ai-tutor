from fastapi import APIRouter, Depends
from writing.services.writing_feedback_services import WritingFeedbackService
from writing.schemas.writing_feedback_schema import WritingFeedback
from writing.helpers.jwt_token_helper import validate_token


writing_feedback_router = APIRouter(tags=["writing_feedback"])
writing_feedback_service = WritingFeedbackService()

@writing_feedback_router.post("/writing-feedback", dependencies = [Depends(validate_token)])
async def grammar_check(text: str) -> WritingFeedback:
    """
    Provide feedback on the given text using the Gemini model.
    """
    

    # Call the grammar check service and return the result
    result = writing_feedback_service.feedback(text)
    return result