import logging

import uvicorn

from src.core.logger import LOGGING
from src.ugc import app

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_config=LOGGING, log_level=logging.DEBUG)
