import abc
import logging


class QueueClient(abc.ABC):
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)

    @abc.abstractmethod
    def send_message(self, queue_name: str, message: str):
        pass

    @abc.abstractmethod
    def consume_messages(self, queue_name: str):
        pass