# YieldWise (Blostem Hackathon MVP)

YieldWise is an AI-powered financial coach built to bridge the gap between people tracking their expenses and truly growing their wealth. It analyzes raw transaction data, identifies a personalized "safe-to-save" surplus, and instantly recommends targeted Fixed Deposit (FD) products. 

This project perfectly mimics the **user-facing discovery layer**, leading directly into the **Blostem FD infrastructure handoff** where the actual multi-bank marketplace, KYC, payments, and servicing would occur.

---

## 🛠 Golden Path Demo Script

Follow these 6 steps to experience the complete end-to-end integration:

1. **Launch the Interface**: Open the Next.js app to see the Landing Page.
2. **Upload CSV**: On the platform, bypass manual entry by uploading the mock transaction CSV (Demo data built-in).
3. **Analyze Dashboard**: View the dynamic Recharts pie/bar charts tracking total spending, income, and emergency buffering logic identifying the "safe-to-save" amount.
4. **Discover the Recommendation**: See the "Why this FD?" section offering a hyper-personalized tenure and amount matching the user's spending volatility score.
5. **Chat Explanation**: Launch the integrated AI Chat coach and ask "Why a 6-month FD instead of 1 year?" for a context-aware defense of the recommendation.
6. **Blostem Handoff**: Proceed to the Booking flow screen. Click "Confirm" to reach the handoff simulation where the payload is sent to Blostem APIs.

---

## 🏗 Architecture & Blostem Integration

The MVP uses a heavily decoupled Client/Server architecture to represent how a consumer-facing FinTech operates on top of Blostem's infrastructure.

```mermaid
graph TD
    A[YieldWise Frontend] -->|1. POST /api/upload| B(FastAPI Backend)
    A -->|2. POST /api/analyze| B
    A -->|3. POST /api/recommend| B
    B -->|4. Business Logic| B
    A -.->|5. Booking Handoff| C[[Blostem Partner API\n(Real World)]]
    
    subgraph Blostem Infrastructure
    C --> D[Multi-Bank Marketplace]
    C --> E[KYC & Auth API]
    C --> F[Payment Gateway]
    C --> G[Servicing & Ledger]
    end
```

### Production Readiness: The Blostem Handoff
In a production setting, the payload from step 6 (`suggestedAmount`, `tenureMonths`, `bankIssuer`) is shipped to the Blostem API endpoints (e.g., `POST /v1/fd/book`). Blostem’s white-label flow would then manage KYC matching, seamless payment rails, and ledger updating, while YieldWise only has to display the returned JSON as a "Booked" state in the UI.

---

## 🚀 API Endpoints

The FastAPI backend securely orchestrates logic using strict Pydantic V2 schemas.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/upload` | Reads CSV text from frontend, parsing & categorizing spending via a heuristic keyword engine. |
| `POST` | `/api/analyze` | Calculates safety buffers and volatility index to derive the `safeToSave` amount safely. |
| `POST` | `/api/recommend` | Maps the safety buffer and stability scores against the active `catalog.py` to yield FDProducts. |
| `POST` | `/api/chat` | Contextually responds to financial inquiries using current user balance buffers. |

---

## 💻 How to Run Locally

Both backend and frontend build completely from scratch out-of-the-box. Ensure you have Python and Node installed.

### 1. Start the Backend (FastAPI)
```bash
cd backend
python -m venv .venv

# Windows activation
.\.venv\Scripts\activate
# Mac/Linux activation
# source .venv/bin/activate

pip install -r requirements.txt
python -m uvicorn main:app --reload
```
*(Runs on `http://localhost:8000`)*

### 2. Start the Frontend (Next.js)
In a secondary terminal tab:
```bash
cd frontend
npm install
npm run dev
```
*(Runs on `http://localhost:3000`)*
