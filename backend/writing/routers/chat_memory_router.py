from fastapi import APIRouter, Depends
from writing.services.chat_memory_service import ChatMemory
from writing.helpers.jwt_token_helper import validate_token

chat_memory_router = APIRouter(tags=["Chat Memory"])

@chat_memory_router.get('/chat_history/{user_id}', dependencies = [Depends(validate_token)])
async def get_chat_history(user_id):
    chat_memory_instance = ChatMemory(user_id=user_id)
    return chat_memory_instance.get_chat_history()

@chat_memory_router.delete('/chat_memory/{user_id}/all', dependencies = [Depends(validate_token)])
async def delete_messages(user_id):
    chat_memory_instance = ChatMemory(user_id=user_id)
    return chat_memory_instance.delete_messages()

@chat_memory_router.delete('/chat_memory/{user_id}/message/{idx}', dependencies = [Depends(validate_token)])
async def delete_message(user_id, idx):
    chat_memory_instance = ChatMemory(user_id=user_id)
    return chat_memory_instance.delete_message(idx)

@chat_memory_router.delete('/chat_memory/{user_id}/last_message', dependencies = [Depends(validate_token)])
async def delete_last_message(user_id):
    chat_memory_instance = ChatMemory(user_id=user_id)
    return chat_memory_instance.delete_last_message()
