import os
import time
import logging
from dotenv import load_dotenv
import requests

from devman_api import wait_for_new_review, configure_api
from logging_config import setup_logging
from telegram_handler import configure_telegram, send_telegram_message
from logic.message_formatter import format_review_message

logger = logging.getLogger("devman_bot")

def process_review(attempt: dict) -> None:
    msg = format_review_message(
        attempt["lesson_title"],
        attempt["is_negative"],
        attempt["lesson_url"],
    )
    send_telegram_message(msg)
    logger.info(f"Проверка обработана: {attempt['lesson_title']}")

def main():
    load_dotenv()
    setup_logging()

    telegram_token     = os.environ["TELEGRAM_BOT_TOKEN"]
    telegram_chat_id   = os.environ["TELEGRAM_CHAT_ID"]
    devman_api_token   = os.environ["DEVMAN_API_TOKEN"]
    devman_longpoll_url = os.getenv(
        "DEVMAN_LONGPOLL_URL",
        "https://dvmn.org/api/long_polling/"
    )

    configure_api(token=devman_api_token, url=devman_longpoll_url)
    configure_telegram(token=telegram_token, chat_id=telegram_chat_id)

    last_timestamp = None
    logger.info("Бот запущен. Ожидаем новые проверки от Devman...")

    while True:
        try:
            response = wait_for_new_review(last_timestamp)
            logger.debug(f"GET-параметры: {response.get('request_query')}")

            if response["status"] == "found":
                for attempt in response["new_attempts"]:
                    process_review(attempt)
                last_timestamp = response["last_attempt_timestamp"]
                logger.debug(f"Обновлён timestamp: {last_timestamp}")

            else:
                logger.info("Нет новых проверок (таймаут)")
                last_timestamp = response["timestamp"]

        except requests.exceptions.ReadTimeout:
            logger.warning("Таймаут сервера Devman — ждём 5 сек.")
            time.sleep(5)

        except requests.exceptions.ConnectionError:
            logger.warning("Проблемы с сетью — ждём 10 сек.")
            time.sleep(10)

        except requests.exceptions.HTTPError as http_err:
            logger.error(f"Devman API ответил ошибкой HTTP: {http_err}")
            time.sleep(30)

        except Exception as err:
            logger.exception(f"Неожиданная ошибка: {err}")
            time.sleep(5)

if __name__ == "__main__":
    main()
