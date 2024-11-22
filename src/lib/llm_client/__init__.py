from src.lib.llm_client.llm_client import LlMClient

def llm_client_factory() -> LlMClient:
    # Importing here to avoid circular imports
    from src.lib.llm_client.openai_llm_client import OpenAiLlMClient
    return OpenAiLlMClient.from_env()