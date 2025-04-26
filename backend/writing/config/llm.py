from llama_index.llms.gemini import Gemini
from dotenv import load_dotenv
import os

# load environment variables from .env file
load_dotenv()


# Gemini
gemini = Gemini(model = "models/gemini-2.0-flash", api_key = os.getenv("GOOGLE_API_KEY"))

# Deepseek

# GPT