# SaveSmart (Blostem Hackathon Project)

SaveSmart is an AI-powered financial coach built to bridge the gap between people tracking their expenses and truly growing their wealth. It uploads transactions, provides intelligent breakdowns of expenses, and intelligently recommends Fixed Deposit (FD) products tailored to the user's "safe-to-save" amount and volatility.

## 🚀 Features Implemented So Far

### 1. Robust AI Python Backend (FastAPI)
The central intelligence of the app has been fully shifted to a Python FastAPI backend to guarantee security, modularity, and future AI LLM insertions.
- **CSV Parsing & Auto-Categorization (`/api/upload`)**: A custom parser reads transaction strings and categorizes expenses (Food, Rent, Shopping, Bills, etc.) based on keyword heuristics.
- **Financial Analyzer (`/api/analyze`)**: Calculates net savings, a dynamic `safe-to-save` algorithm (80% of net, keeping an emergency buffer), and provides a "Stability Score" indicating spending health.
- **Intelligent FD Recommendation Engine (`/api/recommend`)**: Determines the perfect FD tenure and amount based on user financial stability. For example, if a user's expense ratio is volatile, it recommends a short-tenure (6 months) FD to keep cash liquid.
- **Financial Chatbot (`/api/chat`)**: A friendly AI coach that provides guidance on financial terms, emergency funds, and reasons behind specific investment recommendations.

### 2. High-Fidelity Frontend UI (Next.js + Tailwind CSS)
A beautiful, glassmorphic layout tailored for consumer trust and accessibility.
- **Interactive Dashboard**: Incorporates dynamic visualizations using **Recharts** (Pie charts for category breakdowns, Bar charts for monthly trends).
- **FD Booking Flow**: Maps Blostem's structured `FDRecommendation` responses perfectly to a frictionless checkout page featuring DICGC insurance badges and maturity calculations.
- **Conversational UI**: A sleek chat interface allowing users to quickly query their spending and learn about FDs seamlessly. 

### 3. Architecture Refactor (End-to-End)
- **Monolithic to Client/Server Transition**: Cleanly decoupled the initial hardcoded frontend logic. The Next.js frontend now uses `fetch` to push data asynchronously to the Python API. 
- **Type Safety**: Backend uses strict Pydantic V2 models (`alias_generator=to_camel`) perfectly syncing to the TypeScript interfaces on the frontend.
- **Pruned Codebase**: Safely deleted stagnant logic files (`engine.ts`, mock datasets, and markdown scratchpads), keeping only the production components.

---

## 💻 How to Run Locally

### 1. Start the Backend
Navigate to the `backend` directory, activate the python environment, and run FastAPI via uvicorn:
```bash
cd backend
python -m uvicorn main:app --reload
```
*(Backend runs on http://localhost:8000)*

### 2. Start the Frontend
In a new terminal window, navigate to the `frontend` directory and run the Next.js development server:
```bash
cd frontend
npm install
npm run dev
```
*(Frontend runs on http://localhost:3000)*

---
*Built for the Blostem FinTech Hackathon.*
