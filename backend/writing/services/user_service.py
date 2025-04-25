from writing.database import connect_to_mongo
from writing.schemas.user_schema import UserSchema, DeleteUserSchema, UpdateUserSchema
from writing.helpers.security_helper import hash_password, password_validation
from typing import List
from bson import ObjectId
from fastapi import HTTPException

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
                                    is_active = query['is_active'])
            return created_user
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    def get_user(self, user_id: str) -> UserSchema:
        try:
            user_data = self.collection.find_one({"_id": ObjectId(user_id)})
            user = UserSchema(user_id = user_id, username = user_data['username'],  
                            password = user_data['password'], email = user_data['email'],
                            full_name = user_data['full_name'], role = user_data['role'], 
                            is_active = user_data['is_active'])
            return user
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
        
    def get_user_by_email(self, email: str):
        try:
            user_data = self.collection.find_one({"email": email})
            user = UserSchema(user_id = str(user_data['_id']), username = user_data['username'],  
                            password = user_data['password'], email = email,
                            full_name = user_data['full_name'], role = user_data['role'], 
                            is_active = user_data['is_active'])
            return user
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    def get_user_by_username(self, username: str):
        try:
            user_data = self.collection.find_one({"username": username})
            user = UserSchema(user_id = str(user_data['_id']), username = username,  
                            password = user_data['password'], email = user_data['email'],
                            full_name = user_data['full_name'], role = user_data['role'], 
                            is_active = user_data['is_active'])
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
    
    def update_user(self, user_id: str, user: UserSchema) -> UpdateUserSchema:
        try:
            self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": user.dict()})
            return user_id
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    def delete_user(self, user_id: str) -> DeleteUserSchema:
        try:
            self.collection.delete_one({"_id": ObjectId(user_id)})
            message = DeleteUserSchema(user_id = user_id)
            return message
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
