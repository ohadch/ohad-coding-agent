import sys

from openai import OpenAI

from src.lib.llm_client.llm_client import LlMClient
from src.settings import get_settings
from src.types.schema import LlmMessage


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

        return cls(openai_client=client, model=settings.gpt_model)

    def _send_message_implementation_specific_logic(self, message: LlmMessage, **kwargs) -> LlmMessage:
        response = self._openai_client.chat.completions.create(
            model=self._model,
            messages=[
                *self._memory,
                message.model_dump(mode="json")
            ],
            stream=True,
            **kwargs
        )

        response_text = ""

        for chunk in response:
            updated_part = chunk.choices[0].delta.content
            response_text += updated_part

            # Print the updated response to the console by updating the last line and not adding a new line
            print(updated_part, end="", flush=True)


        llm_response = LlmMessage(
            role="assistant",
            content=response_text
        )

        return llm_response
