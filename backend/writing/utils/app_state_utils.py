from fastapi import Request

from writing.services.document_qa_service import DocumentQA
from writing.services.user_service import User


def get_embed_model(request: Request):
    return request.app.state.embed_model


def get_index_instance(user_id, request: Request):
    app_state = request.app.state
    return DocumentQA(
        user_collection=app_state.user_collection,
        storage_context=app_state.storage_context,
        user_id = user_id
    )

def get_user_instance(request: Request):
    app_state = request.app.state
    return User(user_collection=app_state.user_collection)
