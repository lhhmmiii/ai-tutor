from llama_index.llms.gemini import Gemini
import os
from dotenv import load_dotenv
from fastapi import HTTPException
from writing.config.prompts import level_analysis_prompt
from writing.schemas.level_analysis_schema import LevelAnalysis
from llama_index.core.program import LLMTextCompletionProgram
from llama_index.core.output_parsers import PydanticOutputParser

# load environment variables from .env file
load_dotenv()

class LevelAnalysisService:
    """
    Service for analyzing the writing level of a given text using the Gemini model.
    This service utilizes a language model to evaluate the complexity and proficiency
    of the text, providing suggestions for improvement.
    """

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.gemini = Gemini(model="models/gemini-2.0-flash", api_key=self.api_key)

    def analyze_level(self, text: str) -> LevelAnalysis:
        """
        Analyze the writing level of the given text using the Gemini model.

        Args:
            text (str): The text to analyze for writing level.

        Returns:
            LevelAnalysis: The analysis result with level and suggestions.

        Raises:
            HTTPException: If there is an error during the analysis process.
        """
        try:
            program = LLMTextCompletionProgram.from_defaults(
                output_parser=PydanticOutputParser(output_cls=LevelAnalysis),
                prompt_template_str=level_analysis_prompt,
                verbose=True,
                llm=self.gemini,
            )
            response = program(text=text)
            return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error analyzing text level: {str(e)}")