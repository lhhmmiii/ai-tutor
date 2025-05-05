import os
import sys
from typing import Optional

# Thêm đường dẫn cha vào sys.path để import module nội bộ
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from llama_index.core.agent.workflow import ReActAgent
from writing.tools import WritingTools
from writing.config.prompts import writing_tool_selector_prompt
from writing.config.llm import gemini
from writing.services.chat_memory_service import ChatMemory


async def writing_agent(user_id: Optional[str] = "", user_input: str = "") -> str:
    """
    Hàm xử lý tương tác với agent viết văn bản, cung cấp công cụ và phản hồi từ LLM.

    Args:
        user_id (str): ID người dùng để lưu lịch sử trò chuyện.
        user_input (str): Đầu vào của người dùng.

    Returns:
        str: Phản hồi từ tác nhân ReActAgent.
    """
    try:
        # Khởi tạo WritingTools với LLM
        writing_tools = WritingTools(llm=gemini)

        # Tập hợp tất cả công cụ có sẵn
        tools = [
            writing_tools.dictionary_tool,
            writing_tools.grammar_explanation_tool,
            writing_tools.sentence_parsing_tool,
            writing_tools.example_generator,
            writing_tools.conversation_simulator,
            writing_tools.error_correction_tool,
            writing_tools.feedback_tool,
            writing_tools.faq_knowledge_base_tool,
            writing_tools.quick_tips_tool,
            writing_tools.fallback_to_gemini,
        ]

        # Khởi tạo bộ nhớ trò chuyện
        chat_memory = ChatMemory(user_id=user_id).get_chat_memory()

        # Tạo agent với cấu hình hệ thống
        agent = ReActAgent(
            tools=tools,
            llm=gemini,
            system_prompt=writing_tool_selector_prompt,
            verbose=True,
        )

        # Gửi yêu cầu và nhận phản hồi
        response = await agent.run(user_msg=user_input, memory=chat_memory)

        return response

    except Exception as e:
        # Ghi log nếu cần
        print(f"[ERROR] writing_agent: {e}")
        return "An error occurred while processing your request."



# user_input =  "Give me some example sentences using the word 'happy'."

# import asyncio

# result = asyncio.run(writing_agent(user_id="123", user_input = user_input))
# print("Agent Response:\n", result)

