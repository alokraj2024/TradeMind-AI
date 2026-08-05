# TradeMind AI — Project Context

## What this is
An agentic, explainable stock analysis dashboard. User enters a ticker,
the system runs it through a Planner → Analysis → Explanation agent
pipeline and returns a trend call, confidence, risk level, sentiment,
and a plain-English explanation.

## Hard constraints
- No paid API keys anywhere. Market data via `yfinance`. News via
  Yahoo Finance RSS + `feedparser`, with a mock headline fallback.
  Sentiment via `vaderSentiment`. Explanation via template NLG, not an
  LLM call.
- Backend: Python 3.11+, FastAPI. Frontend: React (Vite).
- Every external call (yfinance, RSS) must have a try/except with a
  graceful fallback — never let a network hiccup 500 the endpoint.

## API contract (do not break this shape)
POST /analyze-stock
Request:  { "symbol": "AAPL" }
Response:
{
  "trend": "UP" | "DOWN",
  "confidence": 0.78,
  "risk_level": "LOW" | "MEDIUM" | "HIGH",
  "sentiment_score": 0.72,
  "explanation": "string",
  "signals": {
    "technical": "string",
    "sentiment": "string",
    "risk": "string"
  }
}

## Folder structure (strict — do not reorganize)
/backend
 ├── main.py
 ├── routes/analyze.py
 ├── agents/{planner_agent,analysis_agent,explanation_agent}.py
 ├── services/{market_data,news_service}.py
 ├── engines/{prediction,sentiment,risk}.py
 ├── utils/helpers.py
 ├── data/demo_cache.json
 └── requirements.txt
/frontend
 └── src/{components,pages,services/api.js,App.jsx}
