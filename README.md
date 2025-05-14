# Devman Notifier Bot

Telegram-бот, который уведомляет о результатах проверки заданий на платформе [Devman](https://dvmn.org).

---

## Как это работает

1. Загружает переменные из файла `.env`:
   - `TELEGRAM_BOT_TOKEN` — токен вашего бота  
   - `TELEGRAM_CHAT_ID` — ID чата для уведомлений  
   - `DEVMAN_API_TOKEN` — токен Devman API  
2. Создаёт папку `logs/` и настраивает логгер `devman_bot` с ротацией  
   (500 КБ × 5 файлов).  
3. Запускает цикл long-polling:
   - при `status: found` отправляет уведомления в Telegram;  
   - при штатном таймауте (`ReadTimeout`) немедленно повторяет запрос.  
4. Обрабатывает сетевые сбои (`ConnectionError`) и HTTP-ошибки (`HTTPError`)  
   с требуемой задержкой.  

---

## Структура проекта

```
.
├── bot.py             # Скрипт с основной логикой 
├── requirements.txt   # Зависимости
└── logs/              # Папка для логов (создаётся автоматически)
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

## Деплой на сервер

### Установить systemd-сервис:

1. Скопировать код на сервер:

```bash
git clone git@github.com:Tikhovskoy/devman-review-notifier.git /opt/telegram-bot
```

2. Создать виртуальное окружение и установить зависимости:

```bash
cd /opt/telegram-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Создать файл юнита:

```bash
sudo nano /etc/systemd/system/devmanbot.service
```

Вставить:

```ini
[Unit]
Description=Devman Review Notifier Bot
After=network.target

[Service]
WorkingDirectory=/opt/telegram-bot
ExecStart=/opt/telegram-bot/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

4. Перезапуск сервиса:

```bash
sudo systemctl daemon-reload
sudo systemctl enable devmanbot
sudo systemctl start devmanbot
```

5. Проверка:

```bash
sudo systemctl status devmanbot
sudo journalctl -f -u devmanbot
```

---

## Полезные команды для управления ботом

```bash
# Обновить код
cd /opt/telegram-bot
git pull

# Перезапустить бота
sudo systemctl restart devmanbot

# Смотреть логи
sudo journalctl -f -u devmanbot
```

---

## Описание функций

* **`setup_logging()`**
  Конфигурирует логгер `devman_bot`: добавляет `RotatingFileHandler` с
  ротацией (500 КБ × 5), устанавливает формат сообщений и уровень `INFO`.

* **`format_review_message(lesson_title: str, is_negative: bool, lesson_url: str) → str`**
  Формирует текст уведомления в зависимости от результата проверки:

  * при `is_negative=True` выводит сообщение об ошибках;
  * иначе — что всё прошло успешно.

* **`main()`**
  Основная точка входа:
 
   1. Загружает `.env`.
   2. Создаёт папку логов и настраивает логгер.
   3. Читает все необходимые переменные окружения.

---

## Полезные ссылки

* [Документация Devman API](https://dvmn.org/api/docs/)
* [Telegram Bot API](https://core.telegram.org/bots/api)
