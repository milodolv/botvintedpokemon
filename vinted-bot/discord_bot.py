import requests

from config import DISCORD_WEBHOOK_URL, REQUEST_TIMEOUT


def format_price(price, currency="EUR"):
    if price is None:
        return "Prix inconnu"
    symbol = "€" if currency == "EUR" else currency
    return f"{price:.2f} {symbol}"


def send_startup_message():
    if not DISCORD_WEBHOOK_URL:
        return

    embed = {
        "title": "✅ Bot Pokémon démarré — surveillance active",
        "color": 0x57F287,
        "footer": {"text": "Vinted Pokémon"},
    }

    try:
        requests.post(
            DISCORD_WEBHOOK_URL,
            json={"embeds": [embed]},
            timeout=REQUEST_TIMEOUT,
        )
    except Exception:
        pass


def send_listing(item):
    if not DISCORD_WEBHOOK_URL:
        return

    price_label = format_price(item.get("price"), item.get("currency", "EUR"))
    embed = {
        "title": item.get("title") or "Nouvelle annonce",
        "url": item.get("url"),
        "color": 0x09B1BA,
        "fields": [
            {
                "name": "Prix",
                "value": price_label,
                "inline": True,
            },
            {
                "name": "Lien",
                "value": f"[Voir l'annonce]({item.get('url')})",
                "inline": True,
            },
        ],
        "footer": {"text": "Vinted Pokémon"},
    }

    image_url = item.get("image_url")
    if image_url:
        embed["image"] = {"url": image_url}

    try:
        requests.post(
            DISCORD_WEBHOOK_URL,
            json={"embeds": [embed]},
            timeout=REQUEST_TIMEOUT,
        )
    except Exception:
        pass
