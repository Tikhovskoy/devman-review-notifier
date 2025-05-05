class DevmanAPIError(Exception):
    """Базовая ошибка при работе с Devman API"""


class DevmanTimeoutError(DevmanAPIError):
    """Таймаут при ожидании от Devman"""


class DevmanNetworkError(DevmanAPIError):
    """Ошибка сети при обращении к Devman API"""

class DevmanConnectionError(DevmanAPIError):
    """Сеть недоступна: нет подключения"""
