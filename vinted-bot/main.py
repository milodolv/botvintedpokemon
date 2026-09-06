import time

from config import DISCORD_WEBHOOK_URL, POLL_INTERVAL
from discord_bot import send_listing, send_startup_message
from filters import should_notify
from vinted import VintedClient


def run():
    if not DISCORD_WEBHOOK_URL:
        raise SystemExit("DISCORD_WEBHOOK_URL manquant dans le fichier .env")

    send_startup_message()
    client = VintedClient()
    seen_ids = set()
    first_run = True

    while True:
        try:
            items = client.search_latest()
            new_items = []

            for raw in items:
                parsed = client.parse_item(raw)
                item_id = parsed.get("id")
                if item_id is None or item_id in seen_ids:
                    continue
                seen_ids.add(item_id)
                new_items.append(parsed)

            if first_run:
                first_run = False
            else:
                for item in reversed(new_items):
                    if should_notify(item):
                        send_listing(item)
        except Exception:
            pass

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    run()
