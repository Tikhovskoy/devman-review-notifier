import pytest
from unittest.mock import patch, AsyncMock
from bot import process_review


@pytest.mark.asyncio
async def test_process_review_sends_expected_message():
    attempt = {
        "lesson_title": "Асинхронность в Python",
        "is_negative": False,
        "submitted_at": "2025-05-05T10:00:00.000Z",
        "lesson_url": "https://dvmn.org/lessons/async/"
    }

    with patch("bot.send_telegram_message", new_callable=AsyncMock) as mock_send:
        await process_review(attempt)

        mock_send.assert_awaited_once()
        sent_text = mock_send.call_args[0][0]
        assert "Асинхронность в Python" in sent_text
        assert "всё понравилось" in sent_text
        assert "https://dvmn.org/lessons/async/" in sent_text


@pytest.mark.asyncio
async def test_process_review_sends_message_on_negative_result():
    attempt = {
        "lesson_title": "Алгоритмы",
        "is_negative": True,
        "submitted_at": "2025-05-05T12:00:00.000Z",
        "lesson_url": "https://dvmn.org/lessons/algorithms/"
    }

    with patch("bot.send_telegram_message", new_callable=AsyncMock) as mock_send:
        await process_review(attempt)

        mock_send.assert_awaited_once()
        sent_text = mock_send.call_args[0][0]
        assert "Алгоритмы" in sent_text
        assert "нашлись ошибки" in sent_text
        assert "https://dvmn.org/lessons/algorithms/" in sent_text
