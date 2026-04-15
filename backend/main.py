"""
SaveSmart API — FastAPI backend.
Endpoints: /api/upload, /api/analyze, /api/recommend, /api/chat, /api/catalog
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import (
    AnalyzeRequest, ChatRequest, ChatResponse,
    SpendingSummary, FDRecommendation, Transaction,
)
from engine import parse_csv, analyze, recommend
from chat import respond
from catalog import FD_CATALOG

app = FastAPI(
    title="SaveSmart API",
    description="AI Money Coach backend — spending analysis, FD recommendations, and financial chat.",
    version="1.0.0",
)

# CORS — allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "savesmart-api", "version": "1.0.0"}


@app.post("/api/upload", response_model=list[Transaction])
async def upload_csv(file: UploadFile = File(...)):
    """Upload a CSV file and get parsed, categorized transactions."""
    if not file.filename or not file.filename.endswith(".csv"):
        raise HTTPException(400, "Only CSV files are accepted")

    content = await file.read()
    text = content.decode("utf-8")
    transactions = parse_csv(text)

    if not transactions:
        raise HTTPException(400, "Could not parse any transactions from the CSV")

    return transactions


@app.post("/api/analyze", response_model=SpendingSummary)
def analyze_transactions(req: AnalyzeRequest):
    """Analyze transactions and return spending summary."""
    if not req.transactions:
        raise HTTPException(400, "No transactions provided")
    return analyze(req.transactions)


@app.post("/api/recommend")
def recommend_fd(summary: SpendingSummary):
    """Generate FD recommendation based on spending summary."""
    rec = recommend(summary)
    if not rec:
        raise HTTPException(
            404,
            "Not enough savings to recommend an FD. Safe-to-save amount is below ₹5,000."
        )
    return rec


@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """Get AI-powered financial guidance."""
    if not req.message.strip():
        raise HTTPException(400, "Message cannot be empty")

    reply = respond(req.message, req.summary, req.recommendation)
    return ChatResponse(reply=reply)


@app.get("/api/catalog")
def get_catalog():
    """Get available FD products from Blostem's issuer network."""
    return {
        "issuers": len(FD_CATALOG),
        "products": FD_CATALOG,
        "note": "Rates as of April 2026. Sourced via Blostem's multi-issuer aggregation.",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
