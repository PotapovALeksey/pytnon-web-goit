from mongoengine import Document
from mongoengine.fields import StringField, EnumField, BooleanField
from enum import Enum
import connect


class SmsType(Enum):
    Email = "email"
    Phone = "phone"


class User(Document):
    fullname = StringField(max_length=50, required=True)
    email = StringField(max_length=60, required=True)
    phone = StringField(max_length=60, required=True)
    is_sms_gotten = BooleanField(default=False)
    sms_type = EnumField(SmsType, required=True)
    meta = {"collection": "users"}
