# YieldWise (Blostem Hackathon MVP)

**🔴 Live Demo:** https://yield-wise-66gr.vercel.app/

YieldWise is an AI-powered financial coach that helps users move from expense tracking to wealth-building. It analyzes transaction data, identifies a personalized **safe-to-save** surplus, and recommends suitable fixed deposit (FD) options.

The MVP demonstrates the **user-facing discovery and recommendation layer**, while Blostem represents the **downstream FD infrastructure layer** for multi-bank FD marketplace access, KYC, payments, booking, and servicing in production.

---

## 🛠 Golden Path Demo Script

Follow these 6 steps to experience the complete end-to-end journey:

1. **Launch the Interface**  
   Open the Next.js app and land on the YieldWise home screen.

2. **Upload CSV**  
   Upload the mock transaction CSV (demo data is built in) to bypass manual entry.

3. **Analyze Dashboard**  
   View dynamic Recharts pie/bar charts showing total spending, income, and emergency buffer logic that identifies the **safe-to-save** amount.

4. **Discover the Recommendation**  
   See the **“Why this FD?”** section with a personalized tenure and amount matched to the user’s spending volatility and surplus.

5. **Chat Explanation**  
   Open the integrated AI chat coach and ask questions like _“Why a 6‑month FD instead of 1 year?”_ for a contextual explanation of the recommendation.

6. **Blostem Handoff**  
   Proceed to the booking flow screen. Click **“Confirm”** to reach the **handoff simulation**.  
   In production, this recommendation payload would be forwarded into Blostem’s FD infrastructure for issuer selection, KYC, payments, booking, and servicing.

---

## 🏗 Architecture & Blostem Integration

The MVP uses a decoupled client/server architecture to mirror how a consumer-facing fintech would sit on top of Blostem’s infrastructure. (The Blostem handoff is simulated in this MVP.)

```mermaid
graph TD
    A[YieldWise Frontend] -->|1. POST /api/upload| B(FastAPI Backend)
    A -->|2. POST /api/analyze| B
    A -->|3. POST /api/recommend| B
    A -->|4. POST /api/chat| B
    B -->|5. Business Logic| B
    A -.->|6. Booking Handoff (Simulated)| C["Blostem Partner API<br/>(Real World)"]

    subgraph Blostem Infrastructure
        C --> D[Multi-Bank FD Marketplace]
        C --> E[KYC & Auth]
        C --> F[Payment Rails & Booking Flow]
        C --> G[Servicing & Ledger]
    end
```

In a real deployment, the simulated handoff would be replaced by SDK/API calls to Blostem’s FD stack, which provides access to 10+ bank/NBFC issuers through a single integration and a complete white-label booking flow (KYC, payment, VKYC, and portfolio servicing).

---

## 🔧 Hackathon MVP System Design (High-Level)

YieldWise is an **AI money coach on top of Blostem**. All the intelligence and UX lives in the app; regulated banking work is delegated to Blostem’s rails.

- **Frontend (Next.js + TypeScript + Tailwind)**  
  Dashboard for income/spend/safe‑to‑save, goal setup, AI chat, and an FD recommendation card with a **Book FD** CTA.

- **Backend (FastAPI + PostgreSQL + Redis)**  
  Handles auth, transaction ingest/cleanup, safe‑to‑save computation, recommendation and chat APIs, and a Blostem handoff endpoint.

- **AI Layer (lightweight agents)**  
  A simple orchestrator coordinates:
  - **Budget agent** – categorizes spending
  - **Cashflow agent** – computes safe‑to‑save surplus
  - **FD Suggestion agent** – maps surplus + goal + horizon → suitable FD tenure & amount
  - **Finance Tutor agent** – explains _“why this FD?”_ in plain English

- **Blostem Layer (external)**  
  In production, Blostem provides the FD product catalog, KYC and payment rails, booking journey, and servicing via its API/SDK. YieldWise stays the intelligence + UX layer on top.

➡ For a deeper architecture walkthrough, see [`docs/system-design.md`](./docs/system-design.md).

---

## Current MVP vs Production Plan

| Layer | Current MVP | Production Plan |
| :--- | :--- | :--- |
| **Transaction Input** | Mock CSV upload and built-in sample transactions | Bank/account data ingestion or partner-led financial data sources |
| **Expense Intelligence** | Heuristic parser and categorizer in FastAPI | Improved classification pipeline with learned models and transaction normalization |
| **Recommendation Engine** | Rule-based FD suggestion based on surplus and volatility | Personalized scoring engine using live product catalog, goal timelines, and risk-aware user behavior |
| **Chat / Guidance** | Context-aware rules-based financial coach | RAG-based assistant using FD docs, issuer terms, FAQs, and user context |
| **FD Catalog** | Mock catalog in local backend | Live product and issuer inventory via Blostem integration (10+ bank & NBFC issuers) |
| **Booking Flow** | Simulated handoff screen | Real handoff into Blostem white-label FD journey for KYC, payment, VKYC, and servicing |
| **Post-booking state** | Static success screen | Real booking status, servicing, maturity alerts, and portfolio sync through Blostem rails |

YieldWise is intentionally built as the **AI discovery and recommendation layer** above Blostem’s FD infrastructure. In the MVP, transaction ingestion, recommendation, and booking handoff are simulated with mock data so the end-to-end user journey can be demonstrated clearly. In production, the same UX would connect to Blostem’s live FD infrastructure for multi-bank marketplace access, KYC orchestration, payment rails, booking workflows, and servicing.

---

## RAG & Future Stack

The current MVP uses structured rules and a lightweight contextual coach for speed and reliability. The production design adds a **planned RAG layer** so the assistant can answer using grounded financial context instead of generic LLM responses.

- **Vector DB:** pgvector or Qdrant  
- **Knowledge sources:** Blostem FD product docs, issuer notes, support FAQs, financial literacy material, and user recommendation history  
- **LLM role:** explain _“why this FD?”_, compare tenure choices, answer financial literacy questions, and personalize guidance  
- **Goal:** grounded, explainable responses rather than generic chatbot output

---

## 🚀 API Endpoints

The FastAPI backend orchestrates the core MVP logic using strict Pydantic v2 schemas.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/upload` | Reads CSV text from frontend; parses and categorizes spending via a heuristic keyword engine. |
| `POST` | `/api/analyze` | Calculates safety buffers and a volatility index to derive the `safeToSave` amount. |
| `POST` | `/api/recommend` | Maps the safety buffer and stability scores against the active `catalog.py` to yield FD products. |
| `POST` | `/api/chat` | Responds to financial inquiries using the current user’s balance buffers and recommendation context. |

---

## 💻 How to Run Locally

Both backend and frontend run from scratch. Ensure you have Python and Node installed.

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

Backend runs on: `http://localhost:8000`

### 2. Start the Frontend (Next.js)

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on: `http://localhost:3000`

---

## Why This Fits Blostem

Blostem provides a **single API/SDK integration** to offer fixed deposits from multiple banks and NBFCs, with a complete white-label booking flow covering KYC, payment, VKYC, and portfolio servicing.

YieldWise focuses on the **intelligence and UX layer**:

- understanding user cashflow and goals,  
- computing a safe-to-save surplus,  
- recommending a suitable FD option,  
- and explaining the choice in plain language.

In a production deployment, the recommendation payload from YieldWise would be forwarded into Blostem’s FD infrastructure for issuer selection, KYC orchestration, payment rails, booking workflows, and post-booking servicing. YieldWise remains the user-facing intelligence layer, while Blostem manages the regulated execution layer underneath.
