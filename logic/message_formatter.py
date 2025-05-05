def format_review_message(lesson_title: str, is_negative: bool, lesson_url: str) -> str:
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
