import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "./assets/vite.svg";
import heroImg from "./assets/hero.png";
import "./App.css";

function App() {
  const [symbol, setSymbol] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyzeStock = async () => {
    console.log("BUTTON CLICKED");

    if (!symbol) return;

    setLoading(true);
    setResult(null);

    try {
      // ✅ FIXED API CALL (GET + dynamic symbol)
      const res = await fetch(
        `http://127.0.0.1:8000/analyze/${symbol.toUpperCase()}`
      );

      if (!res.ok) {
        throw new Error("API request failed");
      }

      const data = await res.json();
      console.log("API RESPONSE:", data);

      setResult(data);
    } catch (err) {
      console.error("ERROR:", err);
      setResult({ error: "Failed to fetch data" });
    }

    setLoading(false);
  };

  return (
    <>
      <section id="center">
        <div className="hero">
          <img src={heroImg} className="base" width="170" height="179" alt="" />
          <img src={reactLogo} className="framework" alt="React logo" />
          <img src={viteLogo} className="vite" alt="Vite logo" />
        </div>

        <div>
          <h1>TradeMind AI 🚀</h1>

          <input
            placeholder="Enter stock (AAPL)"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value)}
            style={{
              padding: "10px",
              fontSize: "16px",
              marginRight: "10px",
              borderRadius: "6px",
            }}
          />

          <button
            onClick={analyzeStock}
            style={{
              padding: "10px 16px",
              fontSize: "16px",
              cursor: "pointer",
            }}
          >
            Analyze
          </button>
        </div>

        {/* 🔥 Loading State */}
        {loading && <p style={{ marginTop: "20px" }}>Analyzing...</p>}

        {/* 🔥 Error Handling */}
        {result?.error && (
          <p style={{ color: "red", marginTop: "20px" }}>
            {result.error}
          </p>
        )}

        {/* 🔥 Result Display */}
        {result && !result.error && (
          <div style={{ marginTop: "20px", textAlign: "left" }}>
            <h2>📊 Analysis Result</h2>

            <p><strong>Trend:</strong> {result.trend || "N/A"}</p>
            <p><strong>Confidence:</strong> {result.confidence ?? "N/A"}</p>
            <p><strong>Risk Level:</strong> {result.risk || "N/A"}</p>
            <p><strong>Explanation:</strong> {result.explanation || "N/A"}</p>

            <h3>🔍 Signals</h3>
            <p><strong>Technical:</strong> {result.technical || "N/A"}</p>
            <p><strong>Sentiment:</strong> {result.sentiment || "N/A"}</p>
          </div>
        )}
      </section>

      <div className="ticks"></div>

      <section id="next-steps">
        <div id="docs">
          <h2>Documentation</h2>
          <p>Your questions, answered</p>
        </div>
        <div id="social">
          <h2>Connect with us</h2>
          <p>Join the Vite community</p>
        </div>
      </section>

      <div className="ticks"></div>
      <section id="spacer"></section>
    </>
  );
}

export default App;