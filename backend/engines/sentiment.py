def analyze_sentiment(headlines: list[str]) -> float:
    """Return the average VADER compound score for a list of headlines."""
    if not headlines:
        return 0.0

    try:
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

        analyzer = SentimentIntensityAnalyzer()
        scores = [analyzer.polarity_scores(headline)["compound"] for headline in headlines]
        return round(sum(scores) / len(scores), 2)
    except ImportError:
        print("vaderSentiment is not installed; returning neutral sentiment")
        return 0.0
