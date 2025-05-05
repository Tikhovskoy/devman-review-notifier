import pytest
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
async def test_send_telegram_message_sends_text():
    test_text = "Тестовое сообщение"

    with patch("telegram_handler.Bot", autospec=True) as mock_bot_class:
        mock_bot_instance = mock_bot_class.return_value
        mock_bot_instance.send_message = AsyncMock()

        from telegram_handler import send_telegram_message
        await send_telegram_message(test_text)

        mock_bot_instance.send_message.assert_awaited_once()
        args, kwargs = mock_bot_instance.send_message.call_args
        assert kwargs["text"] == test_text
