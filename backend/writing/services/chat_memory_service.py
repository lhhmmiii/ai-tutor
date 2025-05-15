from llama_index.core.memory import ChatMemoryBuffer
from llama_index.storage.chat_store.redis import RedisChatStore
from fastapi import HTTPException
from typing import Optional

class ChatMemory:
    """
    A class to manage chat memory using Redis as a storage backend.
    """

    def __init__(self, redis_url: str = "redis://localhost:6379", user_id: str = '',
                 ttl: Optional[int] = None):
        """
        Initialize the ChatMemory instance.

        :param redis_url: URL for the Redis server
        :param user_id: Unique identifier for the user
        :param ttl: Time-to-live for chat messages in seconds
        """
        self.redis_url = redis_url
        self.ttl = ttl
        self.user_id = user_id
        self.chat_store = RedisChatStore(redis_url=self.redis_url, ttl=self.ttl)
        self.chat_memory = ChatMemoryBuffer.from_defaults(
            token_limit=100000,
            chat_store=self.chat_store,
            chat_store_key=user_id,
        )

    def get_chat_memory(self):
        """
        Retrieve the chat memory buffer.

        :return: ChatMemoryBuffer instance
        """
        return self.chat_memory

    def get_chat_history(self):
        """
        Retrieve the chat history as a list of messages.

        :return: List of dictionaries containing role and text for each message
        """
        try:
            list_messages = self.chat_memory.get()
            messages = []
            for message in list_messages:
                if str(message.role) == "MessageRole.USER":
                    text = message.blocks[0].text
                    text = text.replace("//", "")
                    text = text.strip()
                    messages.append({'role': 'user', 'text': text})
                else:
                    messages.append({'role': 'assistant', 'text': message.blocks[0].text})
            return messages
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving chat history: {str(e)}")

    def delete_messages(self):
        """
        Delete all messages in chat history.

        :return: Updated ChatMemoryBuffer instance
        """
        try:
            self.chat_store.delete_messages(key=self.user_id)
            return self.chat_memory
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting all messages: {str(e)}")

    def delete_message(self, idx):
        """
        Delete a message in chat history by index.

        :param idx: Index of the message to delete
        :return: Updated ChatMemoryBuffer instance
        """
        try:
            self.chat_store.delete_message(key=self.user_id, idx=int(idx))
            return self.chat_memory
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting message at index {idx}: {str(e)}")

    def delete_last_message(self):
        """
        Delete the last message in chat history.

        :return: Updated ChatMemoryBuffer instance
        """
        try:
            self.chat_store.delete_last_message(key=self.user_id)
            return self.chat_memory
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting last message: {str(e)}")
