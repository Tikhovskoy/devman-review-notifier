# Devman Notifier Bot

Telegram-бот, который уведомляет о результатах проверки заданий на платформе [Devman](https://dvmn.org).

---

## Возможности

- Отслеживает новые проверки работ через Long Polling API Devman
- Автоматически уведомляет в Telegram, когда работа проверена
- Показывает название урока, результат и ссылку на урок
- Обрабатывает сетевые ошибки, таймауты и проблемы с соединением
- Асинхронный, масштабируемый и готовый к продакшену
- Покрыт unit-тестами

---

## Структура проекта

```

devman\_notifier\_bot/
+-- bot.py                   # Точка входа: основной цикл ожидания проверок
+-- config.py                # Переменные окружения (dotenv)
+-- devman\_api.py            # Взаимодействие с API Devman
+-- exceptions.py            # Кастомные исключения
+-- logging\_config.py        # Настройка логирования
+-- telegram\_handler.py      # Отправка сообщений в Telegram
+-- logic/                   # Бизнес-логика
¦   L-- message\_formatter.py # Форматирование сообщений о проверке
+-- logs/
¦   L-- devman\_bot.log       # Файл логов (ротация через logging)
+-- tests/                   # Юнит-тесты
¦   +-- test\_bot.py
¦   +-- test\_message\_formatter.py
¦   L-- test\_telegram\_handler.py
+-- requirements.txt         # Зависимости
+-- README.md                # Документация
L-- **init**.py              # Метка Python-пакета

````

---

## Установка

1. Клонируй репозиторий:

```bash
git clone https://github.com/your-username/devman_notifier_bot.git
cd devman_notifier_bot
````

2. Создай и активируй виртуальное окружение:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Установи зависимости:

```bash
pip install -r requirements.txt
```

4. Создай `.env` файл:

```env
TELEGRAM_BOT_TOKEN=токен_от_BotFather
TELEGRAM_CHAT_ID=твой_чат_ID
DEVMAN_API_TOKEN=токен_от_Devman
```

---

## Запуск

```bash
python bot.py
```

---

## Тестирование

Установи зависимости для тестов (если ещё не установлены):

```bash
pip install -r requirements.txt
```

Запуск тестов:

```bash
PYTHONPATH=. pytest
```

## Принципы архитектуры

* **Разделение ответственности** — каждый модуль выполняет одну задачу
* **Конфигурация через `.env`** — всё чувствительное вынесено в переменные окружения
* **Асинхронность** — используется `aiohttp` и `asyncio`

---

## Полезные ссылки

* [Документация Devman API](https://dvmn.org/api/docs/)
* [Telegram Bot API](https://core.telegram.org/bots/api)
