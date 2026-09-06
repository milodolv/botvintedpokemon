import time

import requests

from config import (
    MAX_BACKOFF,
    PER_PAGE,
    RATE_LIMIT_BACKOFF,
    REQUEST_TIMEOUT,
    SEARCH_ORDER,
    SEARCH_TEXT,
    VINTED_BASE_URL,
)

CHROME_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Origin": VINTED_BASE_URL,
    "Referer": f"{VINTED_BASE_URL}/catalog?search_text={SEARCH_TEXT}&order={SEARCH_ORDER}",
    "Sec-CH-UA": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "X-Requested-With": "XMLHttpRequest",
}


class VintedClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(CHROME_HEADERS)
        self._backoff = RATE_LIMIT_BACKOFF
        self.refresh_session()

    def refresh_session(self):
        try:
            response = self.session.get(
                f"{VINTED_BASE_URL}/catalog",
                params={"search_text": SEARCH_TEXT, "order": SEARCH_ORDER},
                headers={
                    **CHROME_HEADERS,
                    "Accept": (
                        "text/html,application/xhtml+xml,application/xml;"
                        "q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
                    ),
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "none",
                    "Upgrade-Insecure-Requests": "1",
                },
                timeout=REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            cookies = self.session.cookies.get_dict()
            session_id = cookies.get("anonymous-session-id") or cookies.get(
                "anon_id"
            )
            if session_id:
                self.session.headers["Cookie"] = "; ".join(
                    f"{name}={value}" for name, value in cookies.items()
                )
                print(f"Cookie Vinted récupéré : {session_id[:8]}...")
            else:
                print("Cookie Vinted non récupéré")
        except Exception:
            print("Cookie Vinted non récupéré")

    def search_latest(self):
        try:
            response = self.session.get(
                f"{VINTED_BASE_URL}/api/v2/catalog/items",
                params={
                    "search_text": SEARCH_TEXT,
                    "order": SEARCH_ORDER,
                    "page": 1,
                    "per_page": PER_PAGE,
                    "currency": "EUR",
                },
                timeout=REQUEST_TIMEOUT,
            )
            print(f"Status: {response.status_code}, Contenu: {response.text[:300]}")

            if response.status_code in {401, 403}:
                self.refresh_session()
                return []

            if response.status_code == 429:
                time.sleep(self._backoff)
                self._backoff = min(self._backoff * 2, MAX_BACKOFF)
                return []

            response.raise_for_status()
            self._backoff = RATE_LIMIT_BACKOFF
            payload = response.json()
            items = payload.get("items") or []
            print(f"Vinted : {len(items)} items récupérés (status {response.status_code})")
            return items
        except Exception as e:
            print(f"Erreur search Vinted : {e}")
            return []

    @staticmethod
    def parse_item(item):
        item_id = item.get("id")
        title = item.get("title") or "Sans titre"
        price_data = item.get("price") or {}
        if isinstance(price_data, dict):
            amount = price_data.get("amount")
            currency = price_data.get("currency_code") or "EUR"
        else:
            amount = price_data
            currency = item.get("currency") or "EUR"

        try:
            price = float(amount)
        except (TypeError, ValueError):
            price = None

        path = item.get("path") or item.get("url") or ""
        if path.startswith("http"):
            url = path
        elif path:
            url = f"{VINTED_BASE_URL}{path}"
        else:
            url = f"{VINTED_BASE_URL}/items/{item_id}"

        photo = item.get("photo") or {}
        image_url = (
            photo.get("full_size_url")
            or photo.get("url")
            or (item.get("photos") or [{}])[0].get("url")
        )

        return {
            "id": item_id,
            "title": title,
            "price": price,
            "currency": currency,
            "url": url,
            "image_url": image_url,
        }
