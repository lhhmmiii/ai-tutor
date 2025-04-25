from llama_index.core.memory import ChatMemoryBuffer
from llama_index.storage.chat_store.redis import RedisChatStore


class ChatMemory:
    def __init__(self, redis_url: str = "redis://localhost:6379", user_id: str = '',
                 ttl: int = None):
        self.redis_url = redis_url
        self.ttl = ttl
        self.user_id = user_id
        self.chat_store = RedisChatStore(redis_url = self.redis_url, ttl = self.ttl)
        self.chat_memory = ChatMemoryBuffer.from_defaults(
            token_limit=100000,
            chat_store=self.chat_store,
            chat_store_key = user_id,
        )


    def get_chat_history(self):
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

    def delete_messages(self):
        '''
        Delete all messages in chat history
        '''
        self.chat_store.delete_messages(key = self.user_id)
        return self.chat_memory

    def delete_message(self, idx):
        '''
        Delete a message in chat history by idx
        '''
        self.chat_store.delete_message(key = self.user_id, idx = int(idx))
        return self.chat_memory

    def delete_last_message(self):
        self.chat_store.delete_last_message(key = self.user_id)
        return self.chat_memory
