from writing.database import connect_to_mongo
from writing.schemas.user_schema import UserSchema, DeleteUserResponse, UpdateUserResponse
from writing.helpers.security_helper import hash_password, password_validation
from typing import List, Dict, Any, Optional, Union
from bson import ObjectId
from fastapi import HTTPException
import copy

class User:
    """
    A class to manage user-related operations in the database.

    This class provides methods to create, retrieve, update, and delete user records,
    as well as manage user documents within the database.
    """

    def __init__(self, db_name: str, collection_name: str) -> None:
        """
        Initialize the User class with a connection to the specified MongoDB collection.

        :param db_name: The name of the database.
        :param collection_name: The name of the collection within the database.
        """
        self.collection = connect_to_mongo(db_name, collection_name)

    def create_user(self, query: Dict[str, Any]) -> UserSchema:
        """
        Create a new user in the database.

        :param query: A dictionary containing user details.
        :return: A UserSchema object representing the created user.
        :raises HTTPException: If the user already exists or if there is an unexpected error.
        """
        try:
            if self.collection.find_one({"username": query['username']}):
                raise HTTPException(status_code=409, detail="User already exists")
            password = query['password'].get_secret_value()
            if not password_validation(password):
                raise HTTPException(status_code=400, detail="Password is not strong enough")
            hashed_password = hash_password(password)
            query['password'] = hashed_password
            result = self.collection.insert_one(query)
            created_user = UserSchema(user_id=str(result.inserted_id), username=query['username'],
                                      password=query['password'], email=query['email'],
                                      full_name=query['full_name'], role=query['role'],
                                      is_active=query['is_active'], documents=query['documents'])
            return created_user
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    def get_user(self, user_id: str) -> UserSchema:
        """
        Retrieve a user by their ID.

        :param user_id: The ID of the user to retrieve.
        :return: A UserSchema object representing the user.
        :raises HTTPException: If there is an unexpected error.
        """
        try:
            user_data = self.collection.find_one({"_id": ObjectId(user_id)})
            if not user_data:
                raise HTTPException(status_code=404, detail="User not found")
            user = UserSchema(user_id=user_id, username=user_data['username'],
                              password=user_data['password'], email=user_data['email'],
                              full_name=user_data['full_name'], role=user_data['role'],
                              is_active=user_data['is_active'], documents=user_data['documents'])
            return user
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    def get_user_by_email(self, email: str) -> Optional[UserSchema]:
        """
        Retrieve a user by their email address.

        :param email: The email address of the user to retrieve.
        :return: A UserSchema object representing the user.
        :raises HTTPException: If there is an unexpected error.
        """
        try:
            user_data = self.collection.find_one({"email": email})
            if not user_data:
                raise HTTPException(status_code=404, detail="User not found")
            user = UserSchema(user_id=str(user_data['_id']), username=user_data['username'],
                              password=user_data['password'], email=email,
                              full_name=user_data['full_name'], role=user_data['role'],
                              is_active=user_data['is_active'], documents=user_data['documents'])
            return user
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    def get_user_by_username(self, username: str) -> Optional[UserSchema]:
        """
        Retrieve a user by their username.

        :param username: The username of the user to retrieve.
        :return: A UserSchema object representing the user.
        :raises HTTPException: If there is an unexpected error.
        """
        try:
            user_data = self.collection.find_one({"username": username})
            if not user_data:
                raise HTTPException(status_code=404, detail="User not found")
            user = UserSchema(user_id=str(user_data['_id']), username=username,
                              password=user_data['password'], email=user_data['email'],
                              full_name=user_data['full_name'], role=user_data['role'],
                              is_active=user_data['is_active'], documents=user_data['documents'])
            return user
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    def get_users(self) -> List[UserSchema]:
        """
        Retrieve all users from the database.

        :return: A list of UserSchema objects representing all users.
        :raises HTTPException: If there is an unexpected error.
        """
        try:
            users_data = self.collection.find({})
            users: List[UserSchema] = []
            for user_data in users_data:
                user = UserSchema(user_id=str(user_data['_id']), username=user_data['username'],
                                  password=user_data['password'], email=user_data['email'],
                                  full_name=user_data['full_name'], role=user_data['role'],
                                  is_active=user_data['is_active'], documents=user_data.get('documents', []))
                users.append(user)
            return users
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    def update_document_list(self, user_id: str, file_name: str, index_id: Any, ref_doc_ids: List[str]) -> Dict[str, Any]:
        """
        Update the document list for a user.

        :param user_id: The ID of the user whose document list is to be updated.
        :param file_name: The name of the file to add to the document list.
        :param index_id: The index ID associated with the document.
        :param ref_doc_ids: The reference document IDs associated with the document.
        :return: The updated user document.
        :raises HTTPException: If there is an unexpected error.
        """
        try:
            user = self.get_user(user_id)
            documents = user.documents
            document_info = {
                "name": file_name,
                "index_id": index_id,
                "ref_doc_ids": ref_doc_ids,
            }
            documents.append(document_info)
            query_filter = {"_id": ObjectId(user_id)}
            update_operation = {"$set": {"documents": documents}}

            result = self.collection.update_one(query_filter, update_operation)

            if result.modified_count > 0:
                user = self.collection.find_one(query_filter)
                user["_id"] = str(user["_id"])
                return user
            else:
                raise HTTPException(status_code=409, detail="Failed to update user")
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    def update_user(self, user_id: str, user: UserSchema) -> Union[str, None]:
        try:
            user.password = hash_password(user.password)
            self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": user.dict()})
            return user_id
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    def delete_user(self, user_id: str) -> DeleteUserResponse:
        try:
            self.collection.delete_one({"_id": ObjectId(user_id)})
            message = DeleteUserResponse(user_id=user_id)
            return message
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    def delete_document_list(self, index_id: Any, ref_doc_ids: Optional[List[str]]) -> Optional[Dict[str, str]]:
        users = self.get_users()
        for user in users:
            documents = user.documents
            updated_documents = []

            for document in documents:
                if ref_doc_ids is None and document["index_id"] != index_id:
                    updated_documents.append(document)
                elif document["index_id"] == index_id and ref_doc_ids:
                    if ref_doc_ids[0] in document["ref_doc_ids"]:
                        document = copy.deepcopy(document)  # Ensure a deep copy
                        document["ref_doc_ids"].remove(ref_doc_ids[0])
                    updated_documents.append(document)

            if updated_documents != documents:
                query_filter = {"_id": ObjectId(user.user_id)}
                update_operation = {"$set": {"documents": updated_documents}}

                result = self.collection.update_one(query_filter, update_operation)

                if result.modified_count > 0:
                    return {"update user_id": str(user.user_id)}
                else:
                    raise HTTPException(status_code=409, detail="Failed to update user")