from typing import Optional, List, Callable
from llama_index.core.agent.workflow import ReActAgent
from writing.services.chat_memory_service import ChatMemory


class BaseAgentHandler:
    def __init__(
        self,
        agent_name: str,
        llm,
        tools: List[Callable],
        system_prompt: str,
        verbose: bool = False,
    ):
        self.agent_name = agent_name
        self.llm = llm
        self.tools = tools
        self.system_prompt = system_prompt
        self.verbose = verbose

    def build_agent(self) -> ReActAgent:
        return ReActAgent(
            tools=self.tools,
            llm=self.llm,
            system_prompt=self.system_prompt,
            verbose=self.verbose,
        )

    async def run(
        self, user_input: str, user_id: Optional[str] = ""
    ) -> str:
        try:
            memory = ChatMemory(user_id=user_id).get_chat_memory()
            agent = self.build_agent()
            response = await agent.run(user_msg=user_input, memory=memory)
            return response
        except Exception as e:
            print(f"[ERROR] {self.agent_name}: {e}")
            return "An error occurred while processing your request."