from fastapi import APIRouter, Depends
from writing.services.auth_service import Auth
from writing.schemas.user_schema import UserSchema, CreateUserRequest
from writing.schemas.auth_schema import LoginResponseSchema, LogoutResponseSchema, LoginRequest
from fastapi.security import HTTPAuthorizationCredentials
from writing.helpers.jwt_token_helper import reusable_oauth2

auth_router = APIRouter(tags = ["Authentication"])
auth = Auth(db_name = "AI-Tutor", collection_name = "users")


@auth_router.post("/register")
async def register_user(request: CreateUserRequest) -> UserSchema:
    query_params = {'username': request.username, 'password': request.password, 'email': request.email,
                    'full_name': request.full_name, 'role': 'user', 'is_active': False, 'documents': []}
    created_user = auth.register_user(query_params)
    return created_user

@auth_router.post("/login")
async def login_user(login_data: LoginRequest) -> LoginResponseSchema:
    query_params = {'username': login_data.username, 'password': login_data.password}
    return auth.login_user(query_params)


@auth_router.post("/logout")
async def logout_user(token: HTTPAuthorizationCredentials = Depends(reusable_oauth2)) -> LogoutResponseSchema:
    msg = auth.logout_user(token)
    return msg