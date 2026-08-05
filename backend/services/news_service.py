from urllib.parse import quote_plus


def get_news(symbol: str) -> list[str]:
    """Fetch recent Yahoo Finance RSS headlines, with a neutral fallback."""
    fallback = [f"No recent news headlines were available for {symbol}."]
    url = (
        "https://feeds.finance.yahoo.com/rss/2.0/headline?"
        f"s={quote_plus(symbol)}&region=US&lang=en-US"
    )

    try:
        import feedparser

        feed = feedparser.parse(url)
        headlines = [entry.title.strip() for entry in feed.entries if entry.get("title")]
        return headlines[:10] or fallback
    except Exception as error:
        print(f"News fetch failed for {symbol}: {error}")
        return fallback
