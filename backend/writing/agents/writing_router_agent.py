import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from llama_index.core.agent.workflow import ReActAgent
from writing.config.prompts import writing_router_prompt
from writing.tools.writing_tools import GrammarCheckTool, LevevlAnalysisTool, WritingFeedbackTool
from llama_index.llms.gemini import Gemini
from dotenv import load_dotenv


load_dotenv()


api_key = os.getenv("GOOGLE_API_KEY")
gemini = Gemini(model = "models/gemini-2.0-flash", api_key=api_key)

agent  = ReActAgent(
    tools=[GrammarCheckTool, LevevlAnalysisTool, WritingFeedbackTool],
    llm=gemini,
    system_prompt = writing_router_prompt,
    verbose=True,
)

# import asyncio

# text = """
# I realy enjoye walking in the mornig. The air is fresch and the birds are sining. Some times I go to the park and sit on a banch to relax and read a buk. It's a great way 
# to start the day.
# """

# async def main():
#     response = await agent.run(user_msg=f"Please check my grammar: '{text}")
#     print(response)

# if __name__ == "__main__":
#     asyncio.run(main())

