from config import FILTERS_ENABLED, KEYWORDS, MAX_PRICE


def matches_keywords(title):
    text = (title or "").lower()
    return any(keyword.lower() in text for keyword in KEYWORDS)


def matches_price(price):
    if price is None:
        return False
    return price <= MAX_PRICE


def should_notify(item):
    if not FILTERS_ENABLED:
        return True
    return matches_price(item.get("price")) and matches_keywords(item.get("title"))
