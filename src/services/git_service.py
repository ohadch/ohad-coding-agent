import logging

from git import Repo

class GitService:
    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def clone_repo(self, remote_repo_url: str, local_repo_path: str):
        self._logger.info(f"Cloning repo from {remote_repo_url} to {local_repo_path}")

        repo = Repo.clone_from(
            url=remote_repo_url,
            to_path=local_repo_path
        )

        self._logger.info(f"Repo cloned successfully to {local_repo_path}")
        return repo
