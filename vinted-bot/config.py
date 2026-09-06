import os

from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "").strip()

VINTED_BASE_URL = os.getenv("VINTED_BASE_URL", "https://www.vinted.fr").rstrip("/")
SEARCH_TEXT = os.getenv("SEARCH_TEXT", "pokemon")
SEARCH_ORDER = os.getenv("SEARCH_ORDER", "newest_first")
PER_PAGE = int(os.getenv("PER_PAGE", "20"))

POLL_INTERVAL = float(os.getenv("POLL_INTERVAL", "5"))
RATE_LIMIT_BACKOFF = float(os.getenv("RATE_LIMIT_BACKOFF", "30"))
MAX_BACKOFF = float(os.getenv("MAX_BACKOFF", "120"))
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "15"))

FILTERS_ENABLED = os.getenv("FILTERS_ENABLED", "true").lower() in {"1", "true", "yes", "on"}
MAX_PRICE = float(os.getenv("MAX_PRICE", "50"))
KEYWORDS = [
    "pokemon",
    "carte",
    "dracaufeu",
    "pikachu",
    "ex",
    "gx",
    "vmax",
    "gold",
    "full art",
]
