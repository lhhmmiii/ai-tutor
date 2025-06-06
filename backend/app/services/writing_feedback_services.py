from llama_index.llms.gemini import Gemini
import os
from dotenv import load_dotenv
from app.config.prompts import writing_feedback_prompt
from app.schemas.writing_feedback_schema import WritingFeedback
from llama_index.core.program import LLMTextCompletionProgram
from llama_index.core.output_parsers import PydanticOutputParser
from fastapi import HTTPException
from typing import Optional
# load environment variables from .env file
load_dotenv()

class WritingFeedbackService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.gemini = Gemini(model = "models/gemini-2.0-flash", api_key=self.api_key)

    def feedback(self, text: str) -> WritingFeedback:
        """
        Provide feedback on the given text using the Gemini model.
        params:
            text (str): The text to provide feedback on.
        returns:
            str: The feedback on the text.
        """
        try:
            program = LLMTextCompletionProgram.from_defaults(
                output_parser = PydanticOutputParser(output_cls=WritingFeedback),
                prompt_template_str = writing_feedback_prompt,
                verbose=True,
                llm = self.gemini,
            )
            response = program(text = text)
            return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error providing feedback: {str(e)}")