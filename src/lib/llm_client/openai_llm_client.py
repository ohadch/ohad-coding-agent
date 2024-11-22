from openai import OpenAI

from src.lib.llm_client.llm_client import LlMClient
from src.settings import get_settings


class OpenAiLlMClient(LlMClient):

    def __init__(self, openai_client: OpenAI, model: str):
        super().__init__()
        self._openai_client = openai_client
        self._model = model

    @classmethod
    def from_env(cls):
        settings = get_settings()

        client = OpenAI(
            base_url=settings.openai_base_url,
        )

        return cls(openai_client=client, model=settings.openai_model)

    def send_message(self, message: str, role: str = "user", **kwargs) -> str:
        response = self._openai_client.chat.completions.create(
            model=self._model,
            messages=[
                {
                    "role": role,
                    "content": message
                }
            ],
            **kwargs
        )

        return response.choices[0].message.content
