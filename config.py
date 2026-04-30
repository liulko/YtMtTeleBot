from dotenv import load_dotenv
import os
from pathlib import Path

# Визначаємо кореневу папку проєкту
BASE_DIR = Path(__file__).resolve().parent

# Завантажуємо bot.env з правильним шляхом
env_file = BASE_DIR / "bot.env"

if not env_file.exists():
    raise FileNotFoundError(f"Файл не знайдено: {env_file}")

load_dotenv(env_file)

def _get_or_raise(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Обов'язкова змінна середовища відсутня: {key}")
    return value


# Зчитуємо змінні
BOT_TOKEN           = _get_or_raise("BOT_TOKEN")
CHANNEL_ID      = int(_get_or_raise("CHANNEL_ID"))
TELEGRAPH_TOKEN = _get_or_raise("TELEGRAPH_TOKEN")

print("✅ Конфігурація успішно завантажена з bot.env")
print(f"   CHANNEL_ID = {CHANNEL_ID}")
print(f"   BOT_TOKEN  = {BOT_TOKEN[:15]}...")