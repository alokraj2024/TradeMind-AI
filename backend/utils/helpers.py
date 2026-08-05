def sanitize_symbol(symbol: str) -> str:
    """Sanitize and normalize a stock ticker symbol."""
    return symbol.strip().upper()
