import logging

from dotenv import load_dotenv

from src.settings import get_settings

load_dotenv()


from openai import OpenAI

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    settings = get_settings()

    client = OpenAI(
        base_url=settings.openai_base_url,
    )

    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=[
            {
                "role": "user",
                "content": "What is the capital of the United States?"
            }
        ],
        temperature=0,
    )

    print(response.choices[0].message.content)
