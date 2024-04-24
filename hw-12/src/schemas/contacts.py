from datetime import datetime, date

from pydantic import BaseModel, Field, EmailStr


class ContactBaseSchema(BaseModel):
    name: str = Field(max_length=50)
    surname: str = Field(max_length=50)
    email: str = EmailStr()
    phone: str
    birthday: date = None


class ContactSchema(ContactBaseSchema):
    id: int
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        from_attributes = True
