import os
import sys
# Thêm đường dẫn cha vào sys.path để import module nội bộ
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from app.tools import WritingTools
from app.config.prompts import writing_tool_selector_prompt
from app.config.llm import gemini
from app.agents.base import BaseAgentHandler


class WritingAgentHandler(BaseAgentHandler):
    def __init__(self, verbose: bool = True):
        tools = WritingTools(llm=gemini).get_tools()
        super().__init__(
            agent_name="WritingAgent",
            llm=gemini,
            tools=tools,
            system_prompt=writing_tool_selector_prompt,
            verbose=verbose,
        )



# import asyncio

# user_input =  "Give me some example sentences using the word 'happy'."
# async def writing_agent(user_id: str = "", user_input: str = "") -> str:
#     agent = WritingAgentHandler()
#     return await agent.run(user_input=user_input, user_id=user_id)

# if __name__ == "__main__":
#     result = asyncio.run(writing_agent(user_id="123", user_input=user_input))
#     print(result)