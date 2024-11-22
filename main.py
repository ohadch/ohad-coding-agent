from dotenv import load_dotenv
load_dotenv()

import logging

import uvicorn

from src.settings import get_settings

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", force=True
    )

    settings = get_settings()
    uvicorn.run(
        "src:app", host="0.0.0.0", port=settings.port, reload=True, proxy_headers=True
    )
