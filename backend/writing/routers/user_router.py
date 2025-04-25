from fastapi import APIRouter, Depends
from pydantic import SecretStr, EmailStr
from typing import List
from writing.services.user_service import User
from writing.schemas.user_schema import UserSchema, DeleteUserSchema, UpdateUserSchema
from writing.helpers.jwt_token_helper import validate_token

user_router = APIRouter(tags = ["User"])
user_instance = User(db_name = "User_Management", collection_name = "User")

## ---------------------- POST ----------------------
@user_router.post("/user")
async def create_user(username: str, password: SecretStr, email: EmailStr,
                      full_name: str, role: str, is_active: bool) -> UserSchema:
    query_params = {'username': username, 'password': password, 'email': email,
                    'full_name': full_name, 'role': role, 'is_active': is_active}
    created_user = user_instance.create_user(query_params)
    return created_user


## ---------------------- GET ----------------------
@user_router.get("/user/{user_id}", dependencies=[Depends(validate_token)])
async def get_user(user_id: str) -> UserSchema:
    return user_instance.get_user(user_id)

@user_router.get("/user", dependencies=[Depends(validate_token)])
async def get_users() -> List[UserSchema]:
    return user_instance.get_users()

@user_router.get("/user/email/{email}", dependencies=[Depends(validate_token)])
async def get_user_by_email(email: str) -> UserSchema:
    return user_instance.get_user_by_email(email)

@user_router.get("/user/username/{username}", dependencies=[Depends(validate_token)])
async def get_user_by_username(username: str) -> UserSchema:
    return user_instance.get_user_by_username(username)

## ---------------------- PUT ----------------------
@user_router.put("/user/{user_id}", dependencies=[Depends(validate_token)])
async def update_user(user_id: str, user: UserSchema) -> UpdateUserSchema:
    return user_instance.update_user(user_id, user)

## ---------------------- DELETE ----------------------
@user_router.delete("/user/{user_id}", dependencies=[Depends(validate_token)])
async def delete_user(user_id: str) -> DeleteUserSchema:
    return user_instance.delete_user(user_id)