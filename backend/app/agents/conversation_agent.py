import os
import sys
# Thêm đường dẫn cha vào sys.path để import module nội bộ
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from app.tools import ConversationTools
from app.config.prompts import conversation_agent_prompt
from app.config.llm import gemini
from app.agents.base import BaseAgentHandler


class ConversationAgentHandler(BaseAgentHandler):
    def __init__(self, verbose: bool = True):
        tools = ConversationTools(llm=gemini).get_tools()
        super().__init__(
            agent_name="ConversationAgent",
            llm=gemini,
            tools=tools,
            system_prompt=conversation_agent_prompt,
            verbose=verbose,
        )


# import asyncio

# user_input = "As the customer, I said: 'Could I see the menu, please?'"
# async def conversation_agent(user_id: str = "", user_input: str = "") -> str:
#     agent = ConversationAgentHandler()
#     return await agent.run(user_input=user_input, user_id=user_id)

# if __name__ == "__main__":
#     result = asyncio.run(conversation_agent(user_id="123", user_input=user_input))
#     print(result)