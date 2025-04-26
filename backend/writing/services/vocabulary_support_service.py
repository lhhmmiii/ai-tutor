from llama_index.llms.gemini import Gemini
import os
from dotenv import load_dotenv
from writing.config.prompts import generate_vocabulary_prompt
from writing.schemas.vocabulary_support_schema import VocabularyEntry
from llama_index.core.program import LLMTextCompletionProgram
from llama_index.core.output_parsers import PydanticOutputParser

# load environment variables from .env file
load_dotenv()

class VocabularySupportService:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.gemini = Gemini(model = "models/gemini-2.0-flash", api_key=self.api_key)

    def generate(self, text: str) -> str:
        """
        Support user to learn vocabulary more better.
        params:
            text (str): Word, pharse and sentence(if any)
        returns:
            str: A meanings, sentence example, synonym(if any), prompt which is used to generate images
        """
        program = LLMTextCompletionProgram.from_defaults(
            output_parser = PydanticOutputParser(output_cls=VocabularyEntry),
            prompt_template_str = generate_vocabulary_prompt,
            verbose=True,
            llm = self.gemini,
        )
        response = program(text = text)
        return response