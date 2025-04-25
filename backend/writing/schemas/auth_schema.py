from pydantic import BaseModel


class LoginResponseSchema(BaseModel):
    user_id: str
    access_token: str
    message : str = "Login successfully"

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "hjkdfhjklfd5454dfd",
                "access_token": "eyJdfuifduior089t4r067780drf",
            }
        }

class LogoutResponseSchema(BaseModel):
    message: str = "Logout successfully"
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Logout"
            }
        }


