from dotenv import load_dotenv
import os

load_dotenv()  # безпечно: якщо .env немає — просто ігнорується

# ────────────────────────────────────────────────
# Зчитування та перевірка обов'язкових змінних
# ────────────────────────────────────────────────
def _get_or_raise(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Обов'язкова змінна середовища відсутня: {key}")
    return value

BOT_MODE = os.getenv("BOT_MODE", "production").lower()

if BOT_MODE in ("production", "main", "prod"):
    BOT_TOKEN           = _get_or_raise("BOT_TOKEN")
    CHANNEL_ID      = int(_get_or_raise("MAIN_CHANNEL_ID"))
    TELEGRAPH_TOKEN = _get_or_raise("MAIN_TELEGRAPH_TOKEN")
else:
    BOT_TOKEN           = _get_or_raise("BOT_TOKEN")
    CHANNEL_ID      = int(_get_or_raise("TEST_CHANNEL_ID"))
    TELEGRAPH_TOKEN = _get_or_raise("TEST_TELEGRAPH_TOKEN")



