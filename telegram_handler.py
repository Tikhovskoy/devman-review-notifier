import logging
import telegram
from telegram.error import TelegramError

logger = logging.getLogger("devman_bot")

_bot = None
_chat_id = None

def configure_telegram(*, token: str, chat_id: str) -> None:
    global _bot, _chat_id
    _bot = telegram.Bot(token)
    _chat_id = chat_id

def send_telegram_message(text: str) -> None:
    if _bot is None or _chat_id is None:
        raise RuntimeError("Telegram bot is not configured.")
    try:
        _bot.send_message(chat_id=_chat_id, text=text)
    except TelegramError as e:
        logger.error(f"Ошибка отправки сообщения в Telegram: {e}")
