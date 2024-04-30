from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, UUID4

from src.entity.user import Role


class UserInputSchema(BaseModel):
    email: str = EmailStr()
    password: str = Field(min_length=8, max_length=16)


class UserSchema(BaseModel):
    id: UUID4
    email: str
    role: Role
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
