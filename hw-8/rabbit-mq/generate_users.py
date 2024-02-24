from faker import Faker
from models import User, SmsType

fake = Faker()


def generate_users():
    for i in range(20):
        User(
            fullname=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            sms_type=fake.random_element(SmsType).value,
        ).save()
