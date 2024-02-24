import pika
import time
import json
from models import SmsType, User

credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
)
channel = connection.channel()


def callback(ch, method, properties, body):
    message = json.loads(body.decode())

    print(f"[x] Received {message}")

    user = User.objects.get(id=message["user_id"])
    user.update(is_sms_gotten=True)
    time.sleep(0.3)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def consumer_basic(queue: SmsType):
    channel.queue_declare(queue=queue, durable=False)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue, on_message_callback=callback)

    channel.start_consuming()
