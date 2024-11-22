import logging

from src import FeatureRequest
from src.lib.llm_client import llm_client_factory
from src.services.repository_reader_service import RepositoryReaderService


class CodingService:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._llm_client = llm_client_factory()
        self._repo_reader_service = RepositoryReaderService()

    def code_feature(self, feature_request: FeatureRequest):
        file_abs_path_to_content = self._repo_reader_service.read_files(
            feature_request.git_repo_local_path
        )

        # Teach the llm the repo's code
        for file_abs_path, content in file_abs_path_to_content.items():
            self._llm_client.teach(content)
