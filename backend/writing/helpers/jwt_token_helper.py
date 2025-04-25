import jwt
from datetime import datetime, timedelta
from typing import Any, Union
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from pydantic import ValidationError

SECURITY_ALGORITHM = 'HS256'
SECRET_KEY = '1323'

def generate_token(username: Union[str, Any]) -> str:
    expire = datetime.utcnow() + timedelta(
        seconds=60 * 60 * 24  # Expired after 1 day
    )
    to_encode = {
        "exp": expire, "username": username
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=SECURITY_ALGORITHM)
    return encoded_jwt


reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)

def validate_token(http_authorization_credentials=Depends(reusable_oauth2)) -> str:
    """
    Decode JWT token to get username => return username
    """
    # Kiểm tra token có bị logout không
    blacklisted_tokens = [] # Mình sẽ lưu vào DB sau, tạm thời tạo như vầy cho khỏi lỗi đã.
    token = http_authorization_credentials.credentials
    if token in blacklisted_tokens:
        raise HTTPException(status_code=403, detail="Token has been revoked")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[SECURITY_ALGORITHM])
        
        # Lấy thời gian hết hạn của token
        exp_timestamp = payload.get('exp')  
        if exp_timestamp:
            exp_datetime = datetime.fromtimestamp(exp_timestamp)
            if exp_datetime < datetime.now():
                raise HTTPException(status_code=403, detail="Token expired")
            
    except(jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials",
        )