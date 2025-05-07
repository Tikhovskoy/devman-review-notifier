import os
import time
import logging
from dotenv import load_dotenv
import requests
import telegram

from logging_config import setup_logging

logger = logging.getLogger("devman_bot")


def format_review_message(lesson_title: str, is_negative: bool, lesson_url: str) -> str:
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

    bot = telegram.Bot(token=telegram_token)

    last_timestamp = None
    logger.info("Бот запущен. Ожидаем новые проверки от Devman…")

    while True:
        try:
            params = {"timestamp": last_timestamp} if last_timestamp else {}
            headers = {"Authorization": f"Token {devman_api_token}"}

            response = requests.get(
                devman_longpoll_url,
                headers=headers,
                params=params,
                timeout=90
            )
            response.raise_for_status()
            data = response.json()

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
                logger.info("Нет новых проверок (таймаут)")
                last_timestamp = data["timestamp"]

        except requests.exceptions.ReadTimeout:
            logger.debug("Long-polling timeout — повторный запрос")
            continue

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
