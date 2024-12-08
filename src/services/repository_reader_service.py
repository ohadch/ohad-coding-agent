import logging
import os
from typing import Dict, List

import pathspec
from pathspec import PathSpec


class RepositoryReaderService:
    EXCLUDED_FOLDERS = [
        ".git",
        ".idea",
        "venv",
        "__pycache__",
        "node_modules",
    ]

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    @staticmethod
    def _read_gitignore_spec(gitignore_path: str) -> PathSpec:
        with open(gitignore_path, "r") as file:
            gitignore_patterns = file.read()

        # Compile the patterns into a PathSpec object
        spec = pathspec.PathSpec.from_lines('gitwildmatch', gitignore_patterns.splitlines())

        return spec


    # a function that returns a dict of all files under a directory with their content.
    # the key is the absolute path of the file and the value is the content of the file.
    def read_files(
        self, directory: str, include_files: List[str] = None
    ) -> Dict[str, str]:
        # Read .gitignore file if it exists
        if os.path.exists(os.path.join(directory, ".gitignore")):
            gitignore_spec = self._read_gitignore_spec(os.path.join(directory, ".gitignore"))
        else:
            gitignore_spec = None

        file_contents = {}

        # Walk through the directory tree
        for root, _, files in os.walk(directory):
            # Skip excluded folders
            if any(folder in root for folder in self.EXCLUDED_FOLDERS):
                continue

            for file_name in files:
                if include_files and file_name not in include_files:
                    continue

                if gitignore_spec and gitignore_spec.match_file(os.path.relpath(os.path.join(root, file_name), start=directory)):
                    continue

                file_path = os.path.join(root, file_name)

                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        content = file.read()
                        file_contents[file_path] = content
                except Exception as e:
                    print(f"Failed to read {file_path}: {e}")

        return file_contents
