from fastapi import APIRouter
from writing.services.chat_memory_service import ChatMemory

chat_memory_router = APIRouter(tags=["Chat Memory"])

@chat_memory_router.get('/chat_history/{user_id}')
async def get_chat_history(user_id):
    chat_memory_instance = ChatMemory(user_id=user_id)
    return chat_memory_instance.get_chat_history()

@chat_memory_router.delete('/chat_memory/{user_id}/all')
async def delete_messages(user_id):
    chat_memory_instance = ChatMemory(user_id=user_id)
    return chat_memory_instance.delete_messages()

@chat_memory_router.delete('/chat_memory/{user_id}/message/{idx}')
async def delete_message(user_id, idx):
    chat_memory_instance = ChatMemory(user_id=user_id)
    return chat_memory_instance.delete_message(idx)

@chat_memory_router.delete('/chat_memory/{user_id}/last_message')
async def delete_last_message(user_id):
    chat_memory_instance = ChatMemory(user_id=user_id)
    return chat_memory_instance.delete_last_message()
