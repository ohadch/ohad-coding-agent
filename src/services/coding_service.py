import logging

from src import FeatureRequest
from src.lib.llm_client.openai_llm_client import OpenAiLlMClient


class CodingService:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._llm_client = OpenAiLlMClient.from_env()

    def code_feature(self, feature_request: FeatureRequest):
        pass
