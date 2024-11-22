import logging

from src import FeatureRequest


class CodingService:
    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def code_feature(self, feature_request: FeatureRequest):
        raise NotImplementedError