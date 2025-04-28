from pydantic import BaseModel, EmailStr, SecretStr

class UserSchema(BaseModel):
    user_id: str
    username: str
    password: str
    email: EmailStr
    full_name: str
    role: str
    is_active: bool = False

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "lhh1323",
                "username": "LHH",
                "password": "*1323",
                "email": "lehuuhung@example.com",
                "full_name": "Le Huu Hung",
                "role": "admin",
                "is_active": True
            }
        }

class CreateUserRequest(BaseModel):
    username: str
    password: SecretStr
    email: EmailStr
    full_name: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "LHH",
                "password": "*******",
                "email": "lehuuhung@example.com",
                "full_name": "Le Huu Hung",
            }
        }

class UpdateUserResponse(BaseModel):
    user_id: str
    message: str = "User has been updated"

    class Config:
        json_shema_extra = {
            "example": {
                "user_id": "lhh1323",
                "message": "User has been updated"
            }
        }

class DeleteUserResponse(BaseModel):
    user_id: str
    message: str = "User has been deleted"

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "lhh1323",
                "message": "User has been deleted"
            }
        }

