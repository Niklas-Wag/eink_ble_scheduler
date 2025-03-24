import logging
from logging.handlers import RotatingFileHandler

log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s")

file_handler = RotatingFileHandler("../app.log", maxBytes=5 * 1024 * 1024, backupCount=5)
file_handler.setFormatter(log_formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)

logger = logging.getLogger("myApp")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
