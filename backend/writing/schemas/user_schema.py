from pydantic import BaseModel, EmailStr, SecretStr, Field

class UserSchema(BaseModel):
    user_id: str
    username: str
    password: str
    email: EmailStr
    full_name: str
    role: str
    is_active: bool = False
    documents: list[dict] = Field(
        default_factory=list,
        description="List of document items associated with the user",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "lhh1323", 
                "username": "LHH",
                "password": "*1323",
                "email": "lehuuhung@example.com",
                "full_name": "Le Huu Hung",
                "role": "admin",
                "is_active": True,
                "documents": []
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

class UpdateUserRequest(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str
    role: str
    is_active: bool = False
    documents: list[dict] = Field(
        default_factory=list,
        description="List of document items associated with the user",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "username": "LHH",
                "password": "*1323",
                "email": "lehuuhung@example.com",
                "full_name": "Le Huu Hung",
                "role": "admin",
                "is_active": True,
                "documents": []
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

