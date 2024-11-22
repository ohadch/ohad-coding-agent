from dotenv import load_dotenv
load_dotenv()

import logging
import threading

import uvicorn

from src.lib.queue_client.rabbitmq_queue_client import RabbitMqQueueClient
from src.settings import get_settings

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", force=True
    )

    settings = get_settings()

    # Notifications consumer thread
    rabbitmq_client = RabbitMqQueueClient.from_env()

    for queue_name in ["new_feature_requests"]:
        notifications_consumer_thread = threading.Thread(
            target=lambda: rabbitmq_client.consume_messages(queue_name=queue_name), daemon=True
        ).start()

    # Uvicorn thread
    uvicorn.run(
        "src:app", host="0.0.0.0", port=settings.port, reload=True, proxy_headers=True
    )
