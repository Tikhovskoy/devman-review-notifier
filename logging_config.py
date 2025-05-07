import os
import logging
from logging.handlers import RotatingFileHandler

LOG_FILE = os.path.join("logs", "devman_bot.log")
FORMATTER = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
)

def ensure_log_directory() -> None:
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def setup_logging() -> None:
    handler = RotatingFileHandler(LOG_FILE, maxBytes=500_000, backupCount=5)
    handler.setFormatter(FORMATTER)
    logger = logging.getLogger("devman_bot")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

logger = logging.getLogger("devman_bot")
