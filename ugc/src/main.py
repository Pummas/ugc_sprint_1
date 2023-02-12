import logging

import uvicorn

from core.logger import LOGGING
from ugc import app

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001, log_config=LOGGING, log_level=logging.DEBUG)
