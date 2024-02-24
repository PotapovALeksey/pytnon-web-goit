from models import SmsType
from consumer_basic import consumer_basic

if __name__ == "__main__":
    consumer_basic(SmsType.Phone.value)
