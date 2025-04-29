from writing.config.prompts import english_vietnamese_dictionary_prompt, grammar_explanation_prompt, sentence_parsing_prompt,\
                                   example_generator_prompt, conversation_simulator_prompt, error_correction_prompt,\
                                   feedback_prompt, faq_knowledge_base_prompt, quick_tip_prompt, fall_to_gemini_prompt

from writing.config.llm import gemini

class WritingTools:
    def __init__(self, user_id: str = ''):
        self.user_id = user_id

    def dictionary_tool(word: str) -> str:
        """
        Dictionary tool: provide meaning, pronunciation, part of speech, example sentence,
        synonyms, antonyms for a given English word.
        """
        pass

    def grammar_explanation_tool(grammar_point: str) -> str:
        """
        Grammar explanation tool: explain a given English grammar rule,
        provide the rule clearly, how to use, special cases, and examples.
        """
        pass

    def sentence_parsing_tool(sentence: str) -> str:
        """
        Sentence parsing tool: analyze the sentence structure,
        identify parts of speech, clauses, tense, voice, conditionals,
        and provide detailed explanation part-by-part.
        """
        pass

    def example_generator(term: str, category: str = "word") -> str:
        """
        Example generator: generate example sentences for a given word or grammar structure.

        Parameters:
        - term: the target word or grammar structure to create examples for.
        - category: "word" or "grammar" - indicates whether the term is a vocabulary word or a grammar point.

        The output should be several (3-5) example sentences illustrating the use.
        """
        pass

    def conversation_simulator(topic: str) -> str:
        """
        Conversation Simulator: create a realistic dialogue topic, guide user to practice speaking or writing.
        """
        pass


    def error_correction_tool(user_input: str, input_type: str = "text") -> str:
        """
        Error Correction Tool: detect mistakes (grammar, vocabulary, pronunciation if audio),
        suggest corrections, explain errors.

        Parameters:
        - user_input: the text or audio input to check.
        - input_type: "text" or "audio" (if audio, focus on pronunciation errors as well).

        Output should:
        - List errors found.
        - Provide corrected version.
        - Explain each error clearly.
        """

    def feedback_tool(user_response: str, context: str = "") -> str:
        """
        Feedback Tool: evaluate the user's answer,
        highlight strengths and weaknesses,
        and suggest improvements (word choice, grammar, style).

        Parameters:
        - user_response: the sentence or paragraph to evaluate.
        - context: optional, the task or question context.

        Output:
        - Positive feedback.
        - Points to improve.
        - Practical suggestions to enhance language use.
        """

    def faq_knowledge_base_tool(question: str) -> str:
        """
        FAQ Knowledge Base: Provide predefined answers for common questions about
        study tips, pronunciation, listening & speaking practice, and common sentence structures.

        If question matches known FAQ entries, return the answer;
        Otherwise, return empty string to indicate no match.
        """

    def quick_tips_tool(question: str) -> str:
        """
        Quick Tips Tool: Provide short, practical tips or tricks
        related to English learning, grammar, vocabulary, pronunciation, etc.

        The answer should be brief, clear, and actionable.
        """

    def fallback_to_gemini(question: str) -> str:
        """
        Fallback to gemini: If FAQ returns no answer, ask Gemini to generate
        a quick and relevant response to the user's question.
        """