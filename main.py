import logging

from dotenv import load_dotenv
load_dotenv()

from src.settings import OPENAI_BASE_URL, GPT_MODEL

from openai import OpenAI

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    client = OpenAI(
        base_url=OPENAI_BASE_URL
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
