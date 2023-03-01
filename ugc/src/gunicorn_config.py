from core.logger import LOGGING

bind = "0.0.0.0:8001"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
logconfig_dict = LOGGING
