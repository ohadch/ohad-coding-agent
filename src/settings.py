from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    openai_base_url: str
    gpt_model: str


@lru_cache()
def get_settings():
    return Settings()