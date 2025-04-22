from llama_index.llms.gemini import Gemini
from llama_index.core.llms import ChatMessage
import os
from dotenv import load_dotenv
from config.prompts import grammar_check_prompt
from schemas.grammar_check_schema import GrammarCheckResult

# load environment variables from .env file
load_dotenv()

class GrammarCheckService:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.gemini = Gemini(model = "models/gemini-2.0-flash", api_key=self.api_key)

    def structured_llm(self):
        sllm = self.gemini.as_structured_llm(output_cls = GrammarCheckResult)
        return sllm

    def check_grammar(self, text: str) -> str:
        """
        Check the grammar of the given text using the Gemini model.
        params:
            text (str): The text to check for grammar errors.
        returns:
            str: The corrected text with grammar errors fixed.
        """
        messages = [
            ChatMessage(
                role="system",
                content = grammar_check_prompt
            ),
            ChatMessage(
                role="user",
                content=text
            ),
        ]
        # structured_gemini = self.structured_llm()
        response = self.gemini.chat(messages)
        return response