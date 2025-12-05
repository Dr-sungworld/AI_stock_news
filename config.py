import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# Configuration
SCHEDULE_INTERVAL_MINUTES = 10
MARKET_KRX = "KRX"
MARKET_US = "US"

# Watchlist (Example)
WATCHLIST = [
    {"ticker": "005930", "market": MARKET_KRX, "name": "Samsung Electronics"},
    {"ticker": "TSLA", "market": MARKET_US, "name": "Tesla"},
]
