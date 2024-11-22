import json
import logging
import os
from typing import Dict, Optional

from src.lib.llm_client import llm_client_factory
from src.services.repository_reader_service import RepositoryReaderService
from src.utils.exceptions import BadLlmResponseError


class CodingService:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._llm_client = llm_client_factory()
        self._repo_reader_service = RepositoryReaderService()

    def code_feature(self, task: str, local_repo_path: Optional[str] = None) -> Dict[str, str]:
        self._logger.info(f"Asking the llm to code the feature: {task}")

        # Based on the feature request, ask the llm to code the feature.
        # The llm should return a list of files and their updated content.
        file_to_content = self._llm_client.send_message_expecting_json_response(
            f"""
            You are a senior software engineer at a tech company.
            Based on the code i showed you before, I would like to code the following feature: {task}
            As your work may affect multiple files, please return a json response with the following format:
            Do not include any introductory text, just the json response.
            {{ file_path: content }}
            I am going to feed your response directly to a json parser, so it must be valid json.
            """
        )

        if local_repo_path:
            file_to_content = {
                os.path.join(local_repo_path, file_path.replace(local_repo_path, "").lstrip("/")): content
                for file_path, content in file_to_content.items()
            }

        return file_to_content

    def learn_code(self, file_abs_path_to_content: Dict[str, str]):
        self._logger.info("Teaching the llm the code")
        self._llm_client.send_message(
            f"""
            I would like to teach you some code.
            The code is in the following format:
            {{ file_abs_path: content }}
            Here is the code I would like to teach you:
            ===============================================================================================
            {json.dumps(file_abs_path_to_content)}
            ===============================================================================================
            """,
            add_to_memory_without_response=True
        )

        self._logger.info("Taught the llm the code")