import os
import time
import logging
from dotenv import load_dotenv
import requests
import telegram
from logging.handlers import RotatingFileHandler

LOG_FILE = os.path.join("logs", "devman_bot.log")
FORMATTER = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
)

def ensure_log_directory() -> None:
    """Создаёт папку для логов, если её ещё нет."""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def setup_logging() -> None:
    """Настраивает логгер 'devman_bot': handler, формат и уровень INFO."""
    handler = RotatingFileHandler(LOG_FILE, maxBytes=500_000, backupCount=5)
    handler.setFormatter(FORMATTER)
    log = logging.getLogger("devman_bot")
    log.setLevel(logging.INFO)
    log.addHandler(handler)

logger = logging.getLogger("devman_bot")

def format_review_message(
    lesson_title: str, is_negative: bool, lesson_url: str
) -> str:
    """
    Формирует текст уведомления о проверке:
      - если is_negative=True, указывает на ошибки;
      - иначе — что всё хорошо.
    """
    if is_negative:
        return (
            f"У вас проверили работу «{lesson_title}»\n"
            f"К сожалению, в работе нашлись ошибки.\n"
            f"{lesson_url}"
        )
    return (
        f"У вас проверили работу «{lesson_title}»\n"
        f"Преподавателю всё понравилось, можно приступать к следующему уроку.\n"
        f"{lesson_url}"
    )

def main() -> None:
    """
    Запускает бот:
      1. Грузит .env
      2. Создаёт папку логов и настраивает логгер
      3. Читает переменные окружения
      4. Цикл long-polling и отправка в Telegram
    """
    load_dotenv()
    ensure_log_directory()
    setup_logging()

    telegram_token     = os.environ["TELEGRAM_BOT_TOKEN"]
    telegram_chat_id   = os.environ["TELEGRAM_CHAT_ID"]
    devman_api_token   = os.environ["DEVMAN_API_TOKEN"]
    devman_longpoll_url = os.getenv(
        "DEVMAN_LONGPOLL_URL",
        "https://dvmn.org/api/long_polling/"
    )

    bot = telegram.Bot(token=telegram_token)
    last_timestamp = None
    logger.info("Бот запущен. Ожидаем новые проверки от Devman…")

    try:
        while True:
            params = {"timestamp": last_timestamp} if last_timestamp else {}
            headers = {"Authorization": f"Token {devman_api_token}"}

            resp = requests.get(
                devman_longpoll_url,
                headers=headers,
                params=params,
                timeout=90
            )
            resp.raise_for_status()
            data = resp.json()

            if data["status"] == "found":
                for attempt in data["new_attempts"]:
                    msg = format_review_message(
                        attempt["lesson_title"],
                        attempt["is_negative"],
                        attempt["lesson_url"],
                    )
                    bot.send_message(chat_id=telegram_chat_id, text=msg)
                    logger.info(f"Проверка обработана: {attempt['lesson_title']}")
                last_timestamp = data["last_attempt_timestamp"]
                logger.debug(f"Обновлён timestamp: {last_timestamp}")
            else:
                logger.debug("Long-polling timeout — повторный запрос")
                last_timestamp = data["timestamp"]

    except KeyboardInterrupt:
        logger.info("Получен сигнал прерывания — завершаем работу")
        return

if __name__ == "__main__":
    main()
