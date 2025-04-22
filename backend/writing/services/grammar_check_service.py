from llama_index.llms.gemini import Gemini
import os
from dotenv import load_dotenv
from config.prompts import grammar_check_prompt
from schemas.grammar_check_schema import GrammarCheckResult
from llama_index.core.program import LLMTextCompletionProgram
from llama_index.core.output_parsers import PydanticOutputParser

# load environment variables from .env file
load_dotenv()

class GrammarCheckService:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.gemini = Gemini(model = "models/gemini-2.0-flash", api_key=self.api_key)

    def check_grammar(self, text: str) -> str:
        """
        Check the grammar of the given text using the Gemini model.
        params:
            text (str): The text to check for grammar errors.
        returns:
            str: The corrected text with grammar errors fixed.
        """
        program = LLMTextCompletionProgram.from_defaults(
            output_parser = PydanticOutputParser(output_cls=GrammarCheckResult),
            prompt_template_str = grammar_check_prompt,
            verbose=True,
            llm = self.gemini,
        )
        response = program(text = text)
        return response