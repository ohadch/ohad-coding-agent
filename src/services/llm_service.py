from openai import OpenAI


class LlmService:

    def __init__(self):
        settings = get_settings()

        self._client = OpenAI(
            base_url=settings.openai_base_url,
        )
