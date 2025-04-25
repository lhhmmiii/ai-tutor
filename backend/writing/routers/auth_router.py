from fastapi import APIRouter, Depends
from pydantic import SecretStr, EmailStr
from writing.services.auth_service import Auth
from writing.schemas.user_schema import UserSchema
from writing.schemas.auth_schema import LoginResponseSchema, LogoutResponseSchema
from fastapi.security import HTTPAuthorizationCredentials
from writing.helpers.jwt_token_helper import reusable_oauth2

auth_router = APIRouter(tags = ["Authentication"])
auth = Auth(db_name = "User_Management", collection_name = "User")


@auth_router.post("/register")
async def register_user(username: str, password: SecretStr, email: EmailStr,
                        full_name: str) -> UserSchema:
    query_params = {'username': username, 'password': password, 'email': email,
                    'full_name': full_name, 'role': 'user', 'is_active': False}
    created_user = auth.register_user(query_params)
    return created_user


@auth_router.post("/login")
async def login_user(username: str, password: SecretStr) -> LoginResponseSchema:
    query_params = {'username': username, 'password': password}
    return auth.login_user(query_params)


@auth_router.post("/logout")
async def logout_user(token: HTTPAuthorizationCredentials = Depends(reusable_oauth2)) -> LogoutResponseSchema:
    msg = auth.logout_user(token)
    return msg