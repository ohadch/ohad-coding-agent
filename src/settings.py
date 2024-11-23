from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    openai_base_url: str
    openai_api_key: str
    gpt_model: str
    repo_path: str



@lru_cache()
def get_settings():
    return Settings()