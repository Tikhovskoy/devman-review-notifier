import pytest
from logic.message_formatter import format_review_message


def test_negative_review_contains_error_text():
    message = format_review_message(
        lesson_title="Основы Python",
        is_negative=True,
        lesson_url="https://dvmn.org/lesson/123/"
    )
    assert "в работе нашлись ошибки" in message
    assert "Основы Python" in message
    assert "https://dvmn.org/lesson/123/" in message


def test_positive_review_contains_success_text():
    message = format_review_message(
        lesson_title="Основы Django",
        is_negative=False,
        lesson_url="https://dvmn.org/lesson/456/"
    )
    assert "всё понравилось" in message
    assert "можно приступать" in message
    assert "Основы Django" in message
    assert "https://dvmn.org/lesson/456/" in message
