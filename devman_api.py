import aiohttp
import asyncio
from config import DEVMAN_API_TOKEN, DEVMAN_LONGPOLL_URL
from exceptions import (
    DevmanTimeoutError,
    DevmanNetworkError,
    DevmanConnectionError,
)
from logging_config import logger


async def wait_for_new_review(timestamp=None):
    headers = {"Authorization": f"Token {DEVMAN_API_TOKEN}"}
    params = {}
    if timestamp:
        params["timestamp"] = timestamp

    timeout = aiohttp.ClientTimeout(total=90)

    try:
        async with aiohttp.ClientSession(headers=headers, timeout=timeout) as session:
            async with session.get(DEVMAN_LONGPOLL_URL, params=params) as response:
                response.raise_for_status()
                return await response.json()

    except asyncio.TimeoutError as e:
        logger.warning("Таймаут при ожидании Devman API")
        raise DevmanTimeoutError from e

    except aiohttp.ClientConnectionError as e:
        logger.warning("Нет соединения с интернетом (ConnectionError)")
        raise DevmanConnectionError from e

    except aiohttp.ClientError as e:
        logger.error("Ошибка сети при запросе к Devman API")
        raise DevmanNetworkError from e
