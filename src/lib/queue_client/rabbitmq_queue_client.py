import pika

from src.lib.queue_client.queue_client import QueueClient
from src.settings import get_settings


class RabbitMqQueueClient(QueueClient):
    def __init__(self, host: str, port: int, username: str, password: str):
        super().__init__()
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, port=port, credentials=pika.PlainCredentials(username=username, password=password))
        )

    @classmethod
    def from_env(cls):
        settings = get_settings()
        return cls(
            host=settings.rabbitmq_host,
            port=settings.rabbitmq_port,
            username=settings.rabbitmq_user,
            password=settings.rabbitmq_password
        )

    def send_message(self, queue_name: str, message: str):
        self._logger.info(f'Sending message to queue {queue_name}')
        channel = self._connection.channel()
        channel.queue_declare(queue=queue_name)
        channel.basic_publish(exchange='', routing_key=queue_name, body=message)
        self._logger.info(f'Message sent to queue {queue_name}')

    def consume_messages(self, queue_name: str):
        self._logger.info(f'Consuming messages from queue {queue_name}')
        channel = self._connection.channel()
        channel.queue_declare(queue=queue_name)

        def _callback(ch, method, properties, body):
            self._handle_message(
                ch=ch,
                method=method,
                properties=properties,
                body=body
            )

        channel.basic_consume(queue=queue_name, on_message_callback=_callback, auto_ack=True)
        channel.start_consuming()

    def _handle_message(self, ch, method, properties, body):
        print(f'Received message: ch={ch}, method={method}, properties={properties}, body={body}')