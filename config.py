import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
DEVMAN_API_TOKEN = os.getenv("DEVMAN_API_TOKEN")
DEVMAN_LONGPOLL_URL = os.getenv("DEVMAN_LONGPOLL_URL", "https://dvmn.org/api/long_polling/")
