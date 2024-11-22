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

    def checkout(self, local_repo_path: str, source_branch: str, feature_branch: str):
        self._logger.info(f"Checking out branch {feature_branch} from source branch {source_branch} from repo at {local_repo_path}")

        repo = Repo(local_repo_path)

        # If already on the feature branch, return
        if repo.active_branch.name == source_branch:
            self._logger.info(f"Already on branch {feature_branch}")
            return repo

        repo.git.checkout(source_branch)
        repo.git.pull()

        repo.git.checkout(feature_branch)

        self._logger.info(f"Branch {feature_branch} checked out successfully")
        return repo

    def pull(self, local_repo_path: str):
        self._logger.info(f"Pulling latest changes from repo at {local_repo_path}")

        repo = Repo(local_repo_path)
        repo.git.pull()

        self._logger.info(f"Latest changes pulled successfully")
        return repo

