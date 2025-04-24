from llama_index.llms.gemini import Gemini
import os
from dotenv import load_dotenv
from writing.config.prompts import level_analysis_prompt
from writing.schemas.level_analysis_schema import LevelAnalysis
from llama_index.core.program import LLMTextCompletionProgram
from llama_index.core.output_parsers import PydanticOutputParser

# load environment variables from .env file
load_dotenv()

class LevelAnalysisService:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.gemini = Gemini(model = "models/gemini-2.0-flash", api_key=self.api_key)

    def analyze_level(self, text: str) -> str:
        """
        Analyze the writing level of the given text using the Gemini model.
        params:
            text (str): The text to analyze for writing level.
        returns:
            LevelAnalysis: The analysis result with level and suggestions.
        """
        program = LLMTextCompletionProgram.from_defaults(
            output_parser = PydanticOutputParser(output_cls=LevelAnalysis),
            prompt_template_str = level_analysis_prompt,
            verbose=True,
            llm = self.gemini,
        )
        response = program(text = text)
        return response