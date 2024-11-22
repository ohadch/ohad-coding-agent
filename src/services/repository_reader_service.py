import logging
import os
from typing import Dict


class RepositoryReaderService:
    EXCLUDED_FOLDERS = [
        '.git',
        '.idea',
        'venv',
        '__pycache__',
        'node_modules',
    ]

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    # a function that returns a dict of all files under a directory with their content.
    # the key is the absolute path of the file and the value is the content of the file.
    def read_files(self, directory: str) -> Dict[str, str]:
        file_contents = {}

        # Walk through the directory tree
        for root, _, files in os.walk(directory):
            # Skip excluded folders
            if any(folder in root for folder in self.EXCLUDED_FOLDERS):
                continue

            for file_name in files:
                if file_name.startswith('.'):
                    continue

                file_path = os.path.join(root, file_name)

                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        file_contents[file_path] = content
                except Exception as e:
                    print(f"Failed to read {file_path}: {e}")

        return file_contents
