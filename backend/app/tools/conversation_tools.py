from typing import Any, Optional, List, Callable
from app.config.prompts import roleplay_prompt, conversation_feedback_prompt, fall_to_gemini_prompt

class ConversationTools:
    def __init__(self, llm: Optional[Any] = None):
        self.llm = llm

    def get_tools(self) -> List[Callable]:
        return [
            self.conversation_feedback_tool,
            self.roleplay_tool,
        ]

    def conversation_feedback_tool(self, user_input: str = "") -> str:
        """
        Provides friendly and constructive feedback on a completed conversation.

        Use this tool only when the learner asks for feedback or a review of a conversation.
        Examples: "Can you give me feedback?", "How did I do?", "Was my English okay?", etc.

        Args:
            user_input (str): The learner's request for feedback.

        Returns:
            str: Feedback focusing on grammar, vocabulary, fluency, and suggestions for improvement.
        """
        print(333333333333333333)
        return self._run_tool(conversation_feedback_prompt, user_input)


    def roleplay_tool(self, user_input: str = "") -> str:
        """
        Starts or continues a roleplay conversation based on a specific topic, context, and role.

        Use this tool when the learner wants to practice speaking through a real-life scenario.
        Examples: "Let's practice ordering food", "Pretend you're a receptionist", "Simulate a job interview", etc.

        Args:
            user_input (str): The learner's response or request related to the roleplay.

        Returns:
            str: A natural reply based on the assigned role and scenario.
        """
        print(222222222222222222)
        return self._run_tool(roleplay_prompt, user_input)

    
    def fallback_to_gemini(self, user_input: str = "") -> str:
        """
        Answers general questions unrelated to conversation or roleplay.

        Use this tool when the learner asks greeting, vocabulary questions, cultural topics, 
        language tips, or anything not part of a dialogue.
        Examples: "What does this word mean?", "What's the difference between travel and trip?",
        "Any tips to improve fluency?", etc.

        Args:
            user_input (str): The learner's general or unrelated question.

        Returns:
            str: A helpful and informative response to the learner's request.
        """
        print(111111111111111111)
        return self._run_tool(fall_to_gemini_prompt, user_input)

