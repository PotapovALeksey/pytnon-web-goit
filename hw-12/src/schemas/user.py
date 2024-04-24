from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class UserInputSchema(BaseModel):
    email: str = EmailStr()
    password: str = Field(min_length=8, max_length=16)


class UserSchema(BaseModel):
    id: str
    email: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
