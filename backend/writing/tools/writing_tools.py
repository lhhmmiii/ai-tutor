from llama_index.core.llms import ChatMessage
from writing.config.prompts import english_vietnamese_dictionary_prompt, grammar_explanation_prompt, sentence_parsing_prompt,\
                                   example_generator_prompt, conversation_simulator_prompt, error_correction_prompt,\
                                   feedback_prompt, faq_knowledge_base_prompt, quick_tip_prompt, fall_to_gemini_prompt

from typing import List, Callable, Optional, Any

class WritingTools:
    def __init__(self, llm : Optional[Any] = None):
        self.llm = llm
        

    def _run_tool(self, prompt: str, user_input: str) -> str:
        messages = [
            ChatMessage(role="system", content=prompt),
            ChatMessage(role="user", content=user_input),
        ]
        return self.llm.chat(messages)
    
    def get_tools(self) -> List[Callable]:
        return [
            self.dictionary_tool,
            self.grammar_explanation_tool,
            self.sentence_parsing_tool,
            self.example_generator,
            self.conversation_simulator,
            self.error_correction_tool,
            self.feedback_tool,
            self.faq_knowledge_base_tool,
            self.quick_tips_tool,
            self.fallback_to_gemini,
        ]

    def dictionary_tool(self, word: str) -> str:
        """
        Look up an English word and return:
        - Meaning in English and Vietnamese
        - Pronunciation
        - Part of speech
        - Example sentence
        - Synonyms and antonyms
        """
        return self._run_tool(english_vietnamese_dictionary_prompt, word)

    def grammar_explanation_tool(self, grammar_point: str) -> str:
        """
        Explain a specific grammar point clearly, including:
        - Grammar rule
        - Usage
        - Special cases
        - Example sentences
        """
        return self._run_tool(grammar_explanation_prompt, grammar_point)

    def sentence_parsing_tool(self, sentence: str) -> str:
        """
        Parse a sentence and return:
        - Parts of speech
        - Clauses
        - Tense, voice, conditionals
        - Detailed structure explanation
        """
        return self._run_tool(sentence_parsing_prompt, sentence)

    def example_generator(self, term: str, category: str = "word") -> str:
        """
        Generate 3-5 example sentences based on the input.

        Parameters:
        - term: A vocabulary word or grammar structure.
        - category: "word" or "grammar" to guide generation.
        """
        return self._run_tool(example_generator_prompt, f"{category}:{term}")

    def conversation_simulator(self, topic: str) -> str:
        """
        Simulate a conversation on a given topic to help learners
        practice writing or speaking interactively.
        """
        return self._run_tool(conversation_simulator_prompt, topic)

    def error_correction_tool(self, user_input: str, input_type: str = "text") -> str:
        """
        Analyze the user's input and provide:
        - Mistakes (grammar, vocabulary, pronunciation)
        - Corrected version
        - Explanations for each error

        Parameters:
        - input_type: "text" or "audio"
        """
        return self._run_tool(error_correction_prompt, f"<type:{input_type}>\n{user_input}")

    def feedback_tool(self, user_response: str, context: str = "") -> str:
        """
        Give detailed feedback on a user response including:
        - Strengths and weaknesses
        - Suggestions for improvement

        Parameters:
        - context: The question/task the user responded to (optional).
        """
        return self._run_tool(
            feedback_prompt,
            f"<context>{context}</context>\n<response>{user_response}</response>"
        )

    def faq_knowledge_base_tool(self, question: str) -> str:
        """
        Answer frequently asked questions about:
        - Study tips
        - Common grammar/vocabulary patterns
        - Pronunciation and practice advice
        """
        return self._run_tool(faq_knowledge_base_prompt, question)

    def quick_tips_tool(self, question: str) -> str:
        """
        Provide short, actionable tips related to:
        - Grammar
        - Vocabulary
        - Pronunciation
        - English learning strategies
        """
        return self._run_tool(quick_tip_prompt, question)

    def fallback_to_gemini(self, question: str) -> str:
        """
        If no other tool fits the request, use Gemini to generate a
        helpful and relevant response.
        """
        return self._run_tool(fall_to_gemini_prompt, question)