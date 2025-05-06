# Devman Notifier Bot

Telegram-бот, который уведомляет о результатах проверки заданий на платформе [Devman](https://dvmn.org).

---

## Возможности

* Отслеживает новые проверки через Long Polling API Devman
* Автоматически отправляет в Telegram: название урока, результат и ссылку
* Обрабатывает таймауты, ошибки сети и ответы API с кодом ≠200
* Прозрачная конфигурация через `.env` в одном месте (`bot.py`)
* Единый логгер с ротацией (через `logging_config.py`)

---

## Структура проекта

```
devman_notifier_bot/
├── bot.py                   # Точка входа: читаем .env, настраиваем модули и запускаем цикл
├── devman_api.py            # «Чистый» модуль для long-polling Devman API
├── logging_config.py        # Настройка логирования (RotatingFileHandler)
├── telegram_handler.py      # «Чистый» модуль отправки сообщений в Telegram
├── logic/
│   └── message_formatter.py # Форматирование текста уведомлений
├── logs/
│   └── devman_bot.log       # Логи (ротация до 5 файлов по 500 КБ)
├── requirements.txt         # Зависимости проекта
└── README.md                # Эта документация
```

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

## Принципы архитектуры

* **Разделение ответственности**: каждый модуль решает только свою задачу.
* **Единая точка конфигурации**: все переменные окружения читаются в `main()` (`bot.py`).
* **Чистые модули**: `devman_api.py` и `telegram_handler.py` получают настройки через параметры функций.
* **Централизованное логирование**: настраивается один раз в `logging_config.py`, все модули используют `logging.getLogger("devman_bot")`.
* **Обработка ошибок**: ловятся стандартные исключения `requests.exceptions` для таймаутов, сетевых сбоев и HTTP‑ошибок.

---

## Полезные ссылки

* [Документация Devman API](https://dvmn.org/api/docs/)
* [Telegram Bot API](https://core.telegram.org/bots/api)
