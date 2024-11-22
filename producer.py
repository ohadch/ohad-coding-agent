import logging

from dotenv import load_dotenv

from src.lib.queue_client.rabbitmq_queue_client import RabbitMqQueueClient

load_dotenv()

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    queue_client = RabbitMqQueueClient.from_env()
    queue_client.send_message(queue_name='test_queue', message='Hello, world!')