import logging
from logging.handlers import RotatingFileHandler
import os


LOG_FILE = os.path.join("logs", "devman_bot.log")

formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
)

handler = RotatingFileHandler(LOG_FILE, maxBytes=500000, backupCount=5)
handler.setFormatter(formatter)

logger = logging.getLogger("devman_bot")
logger.setLevel(logging.INFO)
logger.addHandler(handler)
