import abc
import logging


class LlMClient(abc.ABC):

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    @abc.abstractmethod
    def send_message(self, message: str, **kwargs) -> str:
        pass