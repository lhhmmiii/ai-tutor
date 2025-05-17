from fastapi import APIRouter, Depends
from typing import List
from app.services.grammar_check_service import GrammarCheckService
from app.schemas.grammar_check_schema import GrammarCheckResult, UpdateGrammarRequest, GrammarResponse
from app.helpers.jwt_token_helper import validate_token


grammar_check_router = APIRouter(tags=["grammar_check"])
grammar_check_service = GrammarCheckService(db_name = "AI-Tutor", collection_name = "grammars")

@grammar_check_router.post("/grammar", dependencies = [Depends(validate_token)])
async def create_grammar(user_id: str, text: str) -> GrammarCheckResult:
    """
    Check the grammar of the given text using the GrammarCheckService.
    """
    

    # Call the grammar check service and return the result
    result = grammar_check_service.create_grammar(user_id = user_id, text = text)
    return result

@grammar_check_router.get("/grammars", dependencies = [Depends(validate_token)])
async def get_grammars(user_id) -> List[GrammarCheckResult]:
    """
    Retrieve grammar correction entries, either all or filtered by user ID.
    """

    # Call the grammar check service and return the result
    result = grammar_check_service.get_grammars(user_id)
    return result

@grammar_check_router.get("/grammar/{grammar_id}", dependencies = [Depends(validate_token)])
async def get_grammar(grammar_id : str) -> GrammarCheckResult:
    """
    Retrieve a single grammar correction entry by its ID.
    """
    

    # Call the grammar check service and return the result
    result = grammar_check_service.get_grammar_by_id(grammar_id)
    return result

@grammar_check_router.put("/grammar/{grammar_id}", dependencies = [Depends(validate_token)])
async def update_grammar(request: UpdateGrammarRequest) -> GrammarResponse:
    """
    Update a grammar correction entry by its ID.
    """
    

    # Call the grammar check service and return the result
    result = grammar_check_service.update_grammar(grammar_id = request.grammar_id, corrected_text=request.grammar.corrected_text,
                                                  issues_found = request.grammar.issues_found)
    respone = GrammarResponse(grammar_id = request.grammar_id, message = "Update successfully")
    return respone

@grammar_check_router.delete("/grammar/{grammar_id}", dependencies = [Depends(validate_token)])
async def delete_grammar(grammar_id: str) -> GrammarResponse:
    """
    Delete a grammar correction entry by its ID.
    """
    

    # Call the grammar check service and return the result
    result = grammar_check_service.delete_grammar(grammar_id)
    respone = GrammarResponse(grammar_id = grammar_id, message = "Delete successfully")
    return respone