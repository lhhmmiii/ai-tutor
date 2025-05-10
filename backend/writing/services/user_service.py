from writing.database import connect_to_mongo
from writing.schemas.user_schema import UserSchema, DeleteUserResponse, UpdateUserResponse
from writing.helpers.security_helper import hash_password, password_validation
from typing import List
from bson import ObjectId
from fastapi import HTTPException
import copy

class User:
    def __init__(self, db_name, collection_name):
        self.collection = connect_to_mongo(db_name, collection_name)

    def create_user(self, query: dict) -> UserSchema:
        try:
            # Check if user already exists
            if self.collection.find_one({"username": query['username']}):
                raise HTTPException(status_code = 409, detail = "User already exists")
            # Password validation
            password = query['password'].get_secret_value()
            if not password_validation(password):
                raise HTTPException(status_code = 400, detail = "Password is not strong enough")
            # Hash the password
            hashed_password = hash_password(password)
            query['password'] = hashed_password
            # Insert user into the collection
            result = self.collection.insert_one(query)
            # Find user by _id
            created_user = UserSchema(user_id = str(result.inserted_id), username = query['username'],  
                                    password = query['password'], email = query['email'],
                                    full_name = query['full_name'], role = query['role'], 
                                    is_active = query['is_active'], documents = query['documents'])
            return created_user
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    def get_user(self, user_id: str) -> UserSchema:
        try:
            user_data = self.collection.find_one({"_id": ObjectId(user_id)})
            user = UserSchema(user_id = user_id, username = user_data['username'],  
                            password = user_data['password'], email = user_data['email'],
                            full_name = user_data['full_name'], role = user_data['role'], 
                            is_active = user_data['is_active'], documents = user_data['documents'])
            print(user)
            return user
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
        
    def get_user_by_email(self, email: str):
        try:
            user_data = self.collection.find_one({"email": email})
            user = UserSchema(user_id = str(user_data['_id']), username = user_data['username'],  
                            password = user_data['password'], email = email,
                            full_name = user_data['full_name'], role = user_data['role'], 
                            is_active = user_data['is_active'], documents = user_data['documents'])
            return user
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    def get_user_by_username(self, username: str):
        try:
            user_data = self.collection.find_one({"username": username})
            user = UserSchema(user_id = str(user_data['_id']), username = username,  
                            password = user_data['password'], email = user_data['email'],
                            full_name = user_data['full_name'], role = user_data['role'], 
                            is_active = user_data['is_active'], documents = user_data['documents'])
            return user
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
        
    
    def get_users(self) -> List[UserSchema]:
        try:
            users_data = self.collection.find({})
            users = []
            for user_data in users_data:
                user = UserSchema(user_id = str(user_data['_id']), username = user_data['username'],
                                password = user_data['password'], email = user_data['email'],
                                full_name = user_data['full_name'], role = user_data['role'],
                                is_active = user_data['is_active'])
                users.append(user)
            return users
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
        
    def update_document_list(self, user_id: str, file_name: str, index_id, ref_doc_ids):
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


    def update_user(self, user_id: str, user: UserSchema) -> UpdateUserResponse:
        try:
            user.password = hash_password(user.password)
            self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": user.dict()})
            return user_id
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    def delete_user(self, user_id: str) -> DeleteUserResponse:
        try:
            self.collection.delete_one({"_id": ObjectId(user_id)})
            message = DeleteUserResponse(user_id = user_id)
            return message
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    def delete_document_list(self, index_id, ref_doc_ids):
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

            print("Original documents:", documents)
            print("Updated documents:", updated_documents)

            if updated_documents != documents:
                query_filter = {"_id": ObjectId(user["_id"])}
                update_operation = {"$set": {"documents": updated_documents}}

                result = self.collection.update_one(query_filter, update_operation)

                if result.modified_count > 0:
                    return {"update user_id": str(user["_id"])}
                else:
                    raise HTTPException(status_code=409, detail="Failed to update user")