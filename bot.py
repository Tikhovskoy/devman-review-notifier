import os
import logging
from dotenv import load_dotenv
import requests
import telegram
from logging.handlers import RotatingFileHandler


logger = logging.getLogger("devman_bot")


class TelegramLogHandler(logging.Handler):
    """Кастомный хэндлер для отправки логов в Telegram."""

    def __init__(self, bot_token, chat_id):
        super().__init__()
        self.bot = telegram.Bot(token=bot_token)
        self.chat_id = chat_id

    def emit(self, record):
        try:
            log_entry = self.format(record)
            self.bot.send_message(chat_id=self.chat_id, text=f"Лог {record.levelname}:\n{log_entry}")
        except Exception as e:
            print(f"Ошибка отправки лога в Telegram: {e}")


def setup_logging(log_file_path: str, bot_token: str, chat_id: str) -> None:
    """Настраивает логгер для systemd, файла и Telegram."""
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(log_file_path, maxBytes=500_000, backupCount=5)
    file_handler.setFormatter(formatter)

    telegram_handler = TelegramLogHandler(bot_token, chat_id)
    telegram_handler.setLevel(logging.ERROR)
    telegram_handler.setFormatter(formatter)

    logger.setLevel(logging.INFO)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(telegram_handler)


def format_review_message(
    lesson_title: str, is_negative: bool, lesson_url: str
) -> str:
    """Формирует текст уведомления о проверке."""
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
    """Запускает бота: загрузка .env, настройка логгера, long-polling."""
    load_dotenv()
    log_file_path = os.path.join("logs", "devman_bot.log")
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    telegram_token = os.environ["TELEGRAM_BOT_TOKEN"]
    telegram_chat_id = os.environ["TELEGRAM_CHAT_ID"]
    devman_api_token = os.environ["DEVMAN_API_TOKEN"]
    devman_longpoll_url = os.getenv(
        "DEVMAN_LONGPOLL_URL",
        "https://dvmn.org/api/long_polling/"
    )

    setup_logging(log_file_path, telegram_token, telegram_chat_id)
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
            review_response = response.json()

            if review_response.get("status") == "found":
                for attempt in review_response["new_attempts"]:
                    msg = format_review_message(
                        attempt["lesson_title"],
                        attempt["is_negative"],
                        attempt["lesson_url"],
                    )
                    bot.send_message(chat_id=telegram_chat_id, text=msg)
                    logger.info(f"Проверка обработана: {attempt['lesson_title']}")
                last_timestamp = review_response.get("last_attempt_timestamp")
                logger.debug(f"Обновлён timestamp: {last_timestamp}")
            else:
                logger.debug("Long-polling timeout — повторный запрос")
                last_timestamp = review_response.get("timestamp")
                if not last_timestamp:
                    logger.warning(f"Нет ключа 'timestamp' в ответе: {review_response}")

    except Exception as e:
        logger.exception(f"Критическая ошибка бота: {e}")
    except KeyboardInterrupt:
        logger.info("Получен сигнал прерывания — завершаем работу")


if __name__ == "__main__":
    main()
