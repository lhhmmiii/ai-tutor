from fastapi import APIRouter
from services.grammar_check_service import GrammarCheckService
# from schemas.grammar_check_schema import GrammarCheckResult


grammar_check_router = APIRouter(tags=["grammar_check"])
grammar_check_service = GrammarCheckService()

@grammar_check_router.post("/grammar-check")
async def grammar_check(text: str):
    """
    Check the grammar of the given text using the GrammarCheckService.
    """
    

    # Call the grammar check service and return the result
    result = grammar_check_service.check_grammar(text)
    return result