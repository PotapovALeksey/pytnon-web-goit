from pydantic import BaseModel


class AuthTokenSchema(BaseModel):
    access_token: str
    refresh_token: str
