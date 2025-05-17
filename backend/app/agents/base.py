import re
from typing import Optional, List, Callable
from llama_index.core.agent.workflow import ReActAgent
from app.services.chat_memory_service import ChatMemory



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
    
    def format_grammar_explanation_as_message(self, text: str) -> str:
        # Bước 1: Tách theo dòng và xử lý từng dòng
        lines = text.strip().split('\n')
        formatted_lines = []
        
        for line in lines:
            stripped = line.strip()

            # Nếu là tiêu đề lớn (có ** ở đầu và cuối)
            if re.match(r"\*\*.+\*\*", stripped):
                formatted_lines.append(f"\n{stripped}\n")

            # Nếu là mục danh sách bắt đầu bằng "* "
            elif re.match(r"^\* ", stripped):
                formatted_lines.append(f"{stripped}")

            # Nếu là ví dụ, cố gắng tách cho dễ đọc hơn
            elif re.search(r"Ví dụ:", stripped, re.IGNORECASE):
                # Nếu chưa có xuống dòng giữa nhãn và ví dụ → tách ra
                if ":" in stripped:
                    parts = stripped.split(":", 1)
                    formatted_lines.append(f"* {parts[0].strip()}:")
                    formatted_lines.append(f"  {parts[1].strip()}")
                else:
                    formatted_lines.append(stripped)

            # Nếu là dòng trắng hoặc không rõ → giữ nguyên hoặc thêm dòng trống nếu cần
            elif stripped == "":
                formatted_lines.append("")
            else:
                formatted_lines.append(f"{stripped}")

        # Bước 2: Ghép lại và đảm bảo không có nhiều dòng trắng liên tiếp
        cleaned_lines = []
        prev_blank = False
        for line in formatted_lines:
            if line.strip() == "":
                if not prev_blank:
                    cleaned_lines.append("")
                prev_blank = True
            else:
                cleaned_lines.append(line)
                prev_blank = False

        return "\n".join(cleaned_lines).strip()

    async def run(
        self, user_input: str, user_id: Optional[str] = ""
    ) -> str:
        try:
            memory = ChatMemory(user_id=user_id).get_chat_memory()
            agent = self.build_agent()
            response = await agent.run(user_msg=user_input, memory=memory)
            print(self.format_grammar_explanation_as_message(response.response.blocks[0].text))
            return self.format_grammar_explanation_as_message(response.response.blocks[0].text)
        except Exception as e:
            print(f"[ERROR] {self.agent_name}: {e}")
            return "An error occurred while processing your request."