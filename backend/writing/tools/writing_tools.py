from llama_index.core.llms import ChatMessage
from writing.config.prompts import english_vietnamese_dictionary_prompt, grammar_explanation_prompt, sentence_parsing_prompt,\
                                   example_generator_prompt, conversation_simulator_prompt, error_correction_prompt,\
                                   feedback_prompt, faq_knowledge_base_prompt, quick_tip_prompt, fall_to_gemini_prompt

from writing.config.llm import gemini

class WritingTools:
    def __init__(self, user_id: str = ''):
        self.user_id = user_id
        self.llm = gemini

    def _run_tool(self, prompt: str, user_input: str) -> str:
        messages = [
            ChatMessage(role="system", content=prompt),
            ChatMessage(role="user", content=user_input),
        ]
        return self.llm.chat(messages)

    def dictionary_tool(self, word: str) -> str:
        return self._run_tool(english_vietnamese_dictionary_prompt, word)

    def grammar_explanation_tool(self, grammar_point: str) -> str:
        return self._run_tool(grammar_explanation_prompt, grammar_point)

    def sentence_parsing_tool(self, sentence: str) -> str:
        return self._run_tool(sentence_parsing_prompt, sentence)

    def example_generator(self, term: str, category: str = "word") -> str:
        return self._run_tool(example_generator_prompt, f"{category}:{term}")

    def conversation_simulator(self, topic: str) -> str:
        return self._run_tool(conversation_simulator_prompt, topic)

    def error_correction_tool(self, user_input: str, input_type: str = "text") -> str:
        return self._run_tool(error_correction_prompt, f"<type:{input_type}>\n{user_input}")

    def feedback_tool(self, user_response: str, context: str = "") -> str:
        return self._run_tool(
            feedback_prompt,
            f"<context>{context}</context>\n<response>{user_response}</response>"
        )

    def faq_knowledge_base_tool(self, question: str) -> str:
        return self._run_tool(faq_knowledge_base_prompt, question)

    def quick_tips_tool(self, question: str) -> str:
        return self._run_tool(quick_tip_prompt, question)

    def fallback_to_gemini(self, question: str) -> str:
        return self._run_tool(fall_to_gemini_prompt, question)