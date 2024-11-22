from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    openai_base_url: str
    gpt_model: str
    sqlalchemy_db_uri: str
    port: int = 8234
    default_page_size: int = 100
    git_repos_path: str = "/tmp/git_repos"
    showcase_repo_path: str = "/tmp/showcase_repo"



@lru_cache()
def get_settings():
    return Settings()