from fastapi import APIRouter, Depends
from writing.services.grammar_check_service import GrammarCheckService
from writing.schemas.grammar_check_schema import GrammarCheckResult
from writing.helpers.jwt_token_helper import validate_token


grammar_check_router = APIRouter(tags=["grammar_check"])
grammar_check_service = GrammarCheckService()

@grammar_check_router.post("/grammar-check", dependencies = [Depends(validate_token)])
async def grammar_check(text: str) -> GrammarCheckResult:
    """
    Check the grammar of the given text using the GrammarCheckService.
    """
    

    # Call the grammar check service and return the result
    result = grammar_check_service.check_grammar(text)
    return result