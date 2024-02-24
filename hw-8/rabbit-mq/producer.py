import pika
from generate_users import generate_users
from models import SmsType, User
from datetime import datetime
import json


credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
)
channel = connection.channel()

EXCHANGE_NAME = "sms_distribution"

channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="topic")
channel.queue_declare(queue=SmsType.Email.value, durable=False)
channel.queue_declare(queue=SmsType.Phone.value, durable=False)

channel.queue_bind(
    exchange=EXCHANGE_NAME, queue=SmsType.Email.value, routing_key=SmsType.Email.value
)
channel.queue_bind(
    exchange=EXCHANGE_NAME, queue=SmsType.Phone.value, routing_key=SmsType.Phone.value
)


def publish_sms():
    users = User.objects.all()

    for user in users:
        parsed_user = user.to_mongo().to_dict()

        message = {
            "user_id": str(parsed_user["_id"]),
            "date": datetime.now().isoformat(),
        }

        channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key=parsed_user["sms_type"],
            body=json.dumps(message).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.TRANSIENT_DELIVERY_MODE
            ),
        )

    connection.close()


if __name__ == "__main__":
    # generate_users()
    publish_sms()
