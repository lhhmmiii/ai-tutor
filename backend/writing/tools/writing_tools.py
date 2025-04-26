import requests
from writing.schemas import GrammarCheckResult, LevelAnalysis, WritingFeedback, VocabularyEntry

API_BASE_URL = "http://127.0.0.1:8000"

def GrammarCheckTool(text: str) -> GrammarCheckResult:
    """
    Check the grammar of the given text.
    params:
        text (str): The text to check for grammar errors.
    returns:
        GrammarCheckResult: The corrected text with grammar errors fixed.
    """
    url = f"{API_BASE_URL}/grammar-check"
    params = {"text": text}
    resp = requests.post(url, params=params)
    resp.raise_for_status()
    return GrammarCheckResult(**resp.json())

def LevevlAnalysisTool(text: str) -> LevelAnalysis:
    """
    Analyze the writing to estimate the English proficiency level.
    params:
        text (str): The text to analyze for English proficiency level.
    returns:
        LevelAnalysis: The analysis of the writing to estimate the English proficiency level.
    """
    url = f"{API_BASE_URL}/level-analysis"
    params = {"text": text}
    resp = requests.post(url, params=params)
    resp.raise_for_status()
    return LevelAnalysis(**resp.json()) 

def WritingFeedbackTool(text: str) -> WritingFeedback:
    """
    Give detailed feedback on coherence, vocabulary, clarity, and tone.
    params:
        text (str): The text to analyze for feedback.
    returns:
        WritingFeedback: The feedback on the writing."""
    url = f"{API_BASE_URL}/writing-feedback"
    params = {"text": text}
    resp = requests.post(url, params=params)
    resp.raise_for_status()
    return WritingFeedback(**resp.json())

def VocabularySupportTool(text: str) -> VocabularyEntry:
    """
    Support user to learn vocabulary more better.
    params:
        text (str): Word, pharse and sentence(if any)
    returns:
        str: A meanings, sentence example, synonym(if any), prompt which is used to generate images
    """
    url = f"{API_BASE_URL}/vocabulary"
    params = {"text": text}
    resp = requests.post(url, params=params)
    resp.raise_for_status()
    return WritingFeedback(**resp.json())