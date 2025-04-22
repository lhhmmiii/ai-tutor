from llama_index.llms.gemini import Gemini
from llama_index.core.llms import ChatMessage
import os
from dotenv import load_dotenv
from config.prompts import level_analysis_prompt
from schemas.level_analysis_schema import LevelAnalysis

# load environment variables from .env file
load_dotenv()

class LevelAnalysisService:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.gemini = Gemini(model = "models/gemini-2.0-flash", api_key=self.api_key)

    def structured_llm(self):
        sllm = self.gemini.as_structured_llm(output_cls = LevelAnalysis)
        return sllm

    def analyze_level(self, text: str) -> str:
        """
        Analyze the writing level of the given text using the Gemini model.
        params:
            text (str): The text to analyze for writing level.
        returns:
            LevelAnalysis: The analysis result with level and suggestions.
        """
        messages = [
            ChatMessage(
                role="system",
                content = level_analysis_prompt,
            ),
            ChatMessage(
                role="user",
                content=text
            ),
        ]
        # structured_gemini = self.structured_llm()
        response = self.gemini.chat(messages)
        return response