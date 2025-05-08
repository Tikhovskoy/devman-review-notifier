import os
import time
import logging
from dotenv import load_dotenv
import requests
import telegram
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("devman_bot")

LOG_FILE = os.path.join("logs", "devman_bot.log")

def setup_logging() -> None:
    """Создаёт папку логов и настраивает логгер: handler, формат и уровень INFO."""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
    )
    handler = RotatingFileHandler(LOG_FILE, maxBytes=500_000, backupCount=5)
    handler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

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
      2. Настраивает логгер
      3. Читает переменные окружения
      4. Цикл long-polling и отправка в Telegram
    """
    load_dotenv()
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

            response = requests.get(
                devman_longpoll_url,
                headers=headers,
                params=params,
                timeout=90
            )
            response.raise_for_status()
            response_data = response.json()

            if response_data["status"] == "found":
                for attempt in response_data["new_attempts"]:
                    msg = format_review_message(
                        attempt["lesson_title"],
                        attempt["is_negative"],
                        attempt["lesson_url"],
                    )
                    bot.send_message(chat_id=telegram_chat_id, text=msg)
                    logger.info(f"Проверка обработана: {attempt['lesson_title']}")
                last_timestamp = response_data["last_attempt_timestamp"]
                logger.debug(f"Обновлён timestamp: {last_timestamp}")
            else:
                logger.debug("Long-polling timeout — повторный запрос")
                last_timestamp = response_data["timestamp"]

    except KeyboardInterrupt:
        logger.info("Получен сигнал прерывания — завершаем работу")
        return

if __name__ == "__main__":
    main()
