from fastapi import APIRouter, Depends
from typing import List
from app.services.user_service import User
from app.schemas.user_schema import UserSchema, UpdateUserResponse, DeleteUserResponse,\
                                        CreateUserRequest, UpdateUserRequest
from app.helpers.jwt_token_helper import validate_token

user_router = APIRouter(tags = ["User"])
user_instance = User(db_name = "AI-Tutor", collection_name = "users")

## ---------------------- POST ----------------------
@user_router.post("/user")
async def create_user(request: CreateUserRequest) -> UserSchema:
    query_params = {'username': request.username, 'password': request.password, 'email': request.email,
                    'full_name': request.full_name, 'role': 'user', 'is_active': False, 'documents': []}
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
async def update_user(user_id: str, user: UpdateUserRequest) -> UpdateUserResponse:
    user_id = user_instance.update_user(user_id, user)
    return UpdateUserResponse(user_id = user_id)

## ---------------------- DELETE ----------------------
@user_router.delete("/user/{user_id}", dependencies=[Depends(validate_token)])
async def delete_user(user_id: str) -> DeleteUserResponse:
    return user_instance.delete_user(user_id)