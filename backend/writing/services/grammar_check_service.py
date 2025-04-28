import os
from dotenv import load_dotenv
from llama_index.llms.gemini import Gemini
from typing import List
from bson import ObjectId
from llama_index.core.program import LLMTextCompletionProgram
from llama_index.core.output_parsers import PydanticOutputParser
from writing.config.prompts import grammar_check_prompt
from writing.schemas.grammar_check_schema import GrammarCheckResult, GrammarIssue
from writing.database import connect_to_mongo

# load environment variables from .env file
load_dotenv()

class GrammarCheckService:
    def __init__(self, api_key: str = None, db_name: str = "", collection_name: str = ""):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.gemini = Gemini(model = "models/gemini-2.0-flash", api_key=self.api_key)
        self.collection = connect_to_mongo(db_name = db_name, collection_name = collection_name)

    def create_grammar(self, user_id: str, text: str) -> GrammarCheckResult:
        """
        Check the grammar of the given text using the Gemini model.
        params:
            text (str): The text to check for grammar errors.
        returns:
            str: The corrected text with grammar errors fixed.
        """
        program = LLMTextCompletionProgram.from_defaults(
            output_parser = PydanticOutputParser(output_cls=GrammarCheckResult),
            prompt_template_str = grammar_check_prompt,
            verbose=True,
            llm = self.gemini,
        )
        response = program(text = text)
        # Query to add DB
        query = {'user_id': user_id, 'corrected_text': response.corrected_text, 'issues_found': []}
        for issue in response.issues_found:
            query['issues_found'].append({'original': issue.original, 'corrected': issue.corrected, 'explanation': issue.explanation})
        # Insert to MongoDB
        result = self.collection.insert_one(query)
        # print(result)
        return response
    
    def get_grammar_by_id(self, grammar_id: str) -> GrammarCheckResult:
        """
        Retrieve a single grammar correction entry by its ID.

        Args:
            grammar_id (str): The ID of the grammar entry to retrieve.

        Returns:
            GrammarCheckResult: The grammar correction entry if found, otherwise None.
        """
        grammar = self.collection.find_one({'_id': ObjectId(grammar_id)})
        if grammar:
            grammar['_id'] = str(grammar['_id'])  # Convert ObjectId to string
            grammar_result = GrammarCheckResult(**grammar)
        return grammar_result

    def get_grammars(self, user_id: str) -> List[GrammarCheckResult]:
        """
        Retrieve grammar correction entries, either all or filtered by user ID.

        Args:
            user_id (Optional[str]): The ID of the user whose corrections to retrieve. If None, retrieves all corrections.

        Returns:
            List[GrammarCheckResult]: A list of grammar correction entries.
        """
        query = {'user_id': user_id} if user_id else {}
        grammars = list(self.collection.find(query))
        results = []
        for grammar in grammars:
            grammar['_id'] = str(grammar['_id'])  # Convert ObjectId to str for easier handling
            grammar_result = GrammarCheckResult(**grammar)
            results.append(grammar_result)
        return grammars
    
    
    def update_grammar(self, grammar_id: str, corrected_text: str = None, issues_found: List[GrammarIssue] = None) -> bool:
        """
        Update a grammar correction entry by its ID.

        Args:
            grammar_id (str): The ID of the grammar entry to update.
            corrected_text (Optional[str]): The new corrected text, if any.
            issues_found (Optional[List[str]]): The updated list of grammar issues found, if any.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        update_fields = {}
        if corrected_text is not None:
            update_fields['corrected_text'] = corrected_text
        if issues_found is not None:
            update_fields['issues_found'] = [issue.dict() for issue in issues_found]

        if not update_fields:
            return False  # Nothing to update

        result = self.collection.update_one(
            {'_id': ObjectId(grammar_id)},
            {'$set': update_fields}
        )
        return result.modified_count == 1

    def delete_grammar(self, grammar_id: str) -> bool:
        """
        Delete a grammar correction entry by its ID.

        Args:
            grammar_id (str): The ID of the grammar entry to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        result = self.collection.delete_one({'_id': ObjectId(grammar_id)})
        return result.deleted_count == 1
    
