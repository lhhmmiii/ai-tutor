import jwt
from datetime import datetime, timedelta
from typing import Any, Union
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from writing.database import redis_client

SECURITY_ALGORITHM = 'HS256'
SECRET_KEY = '1323'
reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)

def generate_token(username: Union[str, Any]) -> str:
    expire = datetime.utcnow() + timedelta(
        seconds=60 * 60 * 24  # Expired after 1 day
    )
    to_encode = {
        "exp": expire, "username": username
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=SECURITY_ALGORITHM)
    return encoded_jwt




def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[SECURITY_ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=403, detail="Invalid token")

def validate_token(http_authorization_credentials=Depends(reusable_oauth2)) -> str:
    token = http_authorization_credentials.credentials

    if redis_client.get(f"blacklist:{token}"):
        raise HTTPException(status_code=403, detail="Token has been revoked")

    payload = decode_token(token)
    exp_timestamp = payload.get("exp")
    if exp_timestamp and datetime.fromtimestamp(exp_timestamp) < datetime.utcnow():
        raise HTTPException(status_code=403, detail="Token expired")
    
    return payload.get("username")
