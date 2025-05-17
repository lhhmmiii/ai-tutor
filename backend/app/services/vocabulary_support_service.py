from llama_index.llms.gemini import Gemini
import os
from dotenv import load_dotenv
from app.config.prompts import generate_vocabulary_prompt
from app.schemas.vocabulary_support_schema import VocabularyEntry, VocabularyResponse
from llama_index.core.program import LLMTextCompletionProgram
from llama_index.core.output_parsers import PydanticOutputParser
from app.database import connect_to_mongo
from fastapi import HTTPException
from typing import Optional
from bson import ObjectId

# load environment variables from .env file
load_dotenv()

class VocabularySupportService:
    def __init__(self, api_key: Optional[str] = None, db_name: str = '', collection_name: str = ''):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.gemini = Gemini(model = "models/gemini-2.0-flash", api_key=self.api_key)
        self.collection = connect_to_mongo(db_name, collection_name)

    def add_word(self, user_id: str, text: str) -> VocabularyResponse:
        """
        Support user to learn vocabulary more better.
        params:
            text (str): Word, phrase and sentence (if any)
        returns:
            VocabularyResponse: The vocabulary entry with meaning, examples, synonyms, and image prompt
        """
        try:
            program = LLMTextCompletionProgram.from_defaults(
                output_parser=PydanticOutputParser(output_cls=VocabularyEntry),
                prompt_template_str=generate_vocabulary_prompt,
                verbose=True,
                llm=self.gemini,
            )
            result = program(text=text)

            query = {
                "user_id": user_id,
                "word": result.word,
                "meaning_vn": result.meaning_vn,
                "sample_sentence": result.sample_sentence,
                "synonyms": result.synonyms,
                "image_idea": result.image_idea,
                "additional_examples": result.additional_examples
            }
            self.collection.insert_one(query)
            return VocabularyResponse(word_id=str(query["_id"]), vocabulary=result)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error adding word: {str(e)}")

    
    def get_word(self, word_id: str) -> VocabularyEntry | None:
        """
        Retrieve a specific vocabulary entry for a user by the given word_id.
        
        Params:
            user_id (str): The ID of the user.
            word_id (str): The word_id of the vocabulary word to find.
        
        Returns:
            VocabularyEntry | None: Returns a VocabularyEntry instance if found, otherwise None.
        """
        try:
            data = self.collection.find_one({"_id": ObjectId(word_id)})
            if not data:
                raise HTTPException(status_code=404, detail="Word not found")
            data.pop("_id")
            return VocabularyEntry(**data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving word: {str(e)}")


    def get_words(self, user_id: str) -> tuple[list[str], list[VocabularyEntry]]:
        """
        Retrieve all vocabulary entries for a specific user.
        
        Params:
            user_id (str): The ID of the user.
        
        Returns:
            list[VocabularyEntry]: A list of VocabularyEntry objects. Returns an empty list if none found.
        """
        try:
            cursor = self.collection.find({"user_id": user_id})
            results = []
            word_ids = []
            for data in cursor:
                word_id = str(data.pop("_id"))
                word_ids.append(word_id)
                results.append(VocabularyEntry(**data))
            return word_ids, results
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving words: {str(e)}")


    def update_word(self, word_id: str, updated_fields: dict) -> str:
        """
        Update fields of a vocabulary entry for a user.
        
        Params:
            user_id (str): The ID of the user.
            word_id (str): The MongoID of the vocabulary word to update.
            updated_fields (dict): A dictionary of fields to update with their new values.
        
        Returns:
            bool: True if the update was successful (found and modified), False otherwise.
        """
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(word_id)},
                {"$set": updated_fields.dict()}
            )
            if result.modified_count == 0:
                raise HTTPException(status_code=404, detail="Word not found or no changes made")
            return "Update successfully"
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating word: {str(e)}")


    def delete_word(self, word_id: str) -> bool:
        """
        Delete a vocabulary entry for a user by word_id.
        
        Params:
            user_id (str): The ID of the user.
            word_id (str): The MongoID of the vocabulary word to delete.
        
        Returns:
            bool: True if the deletion was successful (found and deleted), False otherwise.
        """
        try:
            from bson import ObjectId
            result = self.collection.delete_one({"_id": ObjectId(word_id)})
            if result.deleted_count == 0:
                raise HTTPException(status_code=404, detail="Word not found")
            return True
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting word: {str(e)}")
