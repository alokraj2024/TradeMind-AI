import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ✅ IMPORTANT: correct import
from routes.analyze import router as analyze_router

app = FastAPI(title="TradeMind AI", version="0.1.0")

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ THIS LINE IS CRITICAL
app.include_router(analyze_router)


@app.get("/")
def root():
    return {"message": "TradeMind AI Backend Running 🚀"}


@app.get("/health")
def health_check():
    return {"status": "ok"}