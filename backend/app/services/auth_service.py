from fastapi import HTTPException
from app.services.user_service import User  
from app.schemas.user_schema import UserSchema
from app.schemas.auth_schema import LoginResponseSchema
from app.helpers.security_helper import verify_password
from app.helpers.jwt_token_helper import generate_token, decode_token
from datetime import datetime
from app.database import redis_client
from typing import Dict



class Auth:
    def __init__(self, db_name: str, collection_name: str):
        self.user = User(db_name=db_name, collection_name=collection_name)

    def register_user(self, query: dict) -> UserSchema:
        try:
            new_user = self.user.create_user(query)
            return new_user
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def login_user(self, query: dict) -> LoginResponseSchema:
        try:
            username = query['username']
            user = self.user.get_user_by_username(username)
            if user:
                if verify_password(query['password'].get_secret_value(), user.password):
                    token = generate_token(username)
                    return LoginResponseSchema(user_id=user.user_id, access_token=token)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def logout_user(self, token) -> Dict[str, str]:
        try:
            token_str = token.credentials
            payload = decode_token(token_str)

            exp_timestamp = payload.get("exp")
            ttl = exp_timestamp - int(datetime.utcnow().timestamp())

            redis_client.setex(f"blacklist:{token_str}", ttl, "revoked")
            return {"message": "Logout successful"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
