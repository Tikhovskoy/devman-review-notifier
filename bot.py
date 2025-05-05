from devman_api import wait_for_new_review
from exceptions import (
    DevmanTimeoutError,
    DevmanNetworkError,
    DevmanConnectionError,
)
from logging_config import logger
from telegram_handler import send_telegram_message
from logic.message_formatter import format_review_message


async def process_review(attempt: dict) -> None:
    """Формирует и отправляет сообщение в Telegram о результатах проверки."""
    message = format_review_message(
        attempt["lesson_title"],
        attempt["is_negative"],
        attempt["lesson_url"],
    )
    await send_telegram_message(message)
    logger.info(f"Проверка обработана: {attempt['lesson_title']}")


async def main():
    """Основной цикл ожидания и обработки новых проверок."""
    last_timestamp = None
    logger.info("Бот запущен. Ожидаем новые проверки от Devman...")

    while True:
        try:
            response = await wait_for_new_review(last_timestamp)
            logger.debug(f"Запрос выполнен. GET параметры: {response.get('request_query')}")

            if response["status"] == "found":
                for attempt in response["new_attempts"]:
                    await process_review(attempt)
                last_timestamp = response["last_attempt_timestamp"]
                logger.debug(f"Обновлён timestamp (после found): {last_timestamp}")

            elif response["status"] == "timeout":
                logger.info("Нет новых проверок (таймаут сервера Devman)")
                last_timestamp = response["timestamp"]

        except DevmanConnectionError:
            logger.warning("Отключение интернета — повтор через 10 сек")
            await asyncio.sleep(10)

        except (DevmanTimeoutError, DevmanNetworkError):
            await asyncio.sleep(5)

        except Exception as error:
            logger.exception(f"Необработанная ошибка: {error}")
            await asyncio.sleep(5)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
