const API_BASE_URL = "http://localhost:8000";

export async function analyzeStock(symbol) {
  const response = await fetch(`${API_BASE_URL}/analyze-stock`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ symbol }),
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}

export async function healthCheck() {
  const response = await fetch(`${API_BASE_URL}/health`);
  return response.json();
}
