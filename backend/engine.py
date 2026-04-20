"""
Core engine — CSV parsing, spending analysis, FD recommendation.
This is the "brain" of SaveSmart, now living server-side.
"""

import csv
import io
import math
from datetime import datetime
from collections import defaultdict

from models import (
    Transaction, SpendingSummary, CategoryBreakdown, MonthlyTrend,
    FDProduct, FDRecommendation,
)
from catalog import FD_CATALOG, CATEGORY_CONFIG, CATEGORY_KEYWORDS


# ─────────────────────────────────────────────────────────────────
# 1. Budget Agent
# ─────────────────────────────────────────────────────────────────

class BudgetAgent:
    """Agent responsible for cleaning and categorizing raw spending data."""

    @staticmethod
    def categorize(description: str) -> str:
        """Auto-detect category from transaction description."""
        lower = description.lower()
        for cat, keywords in CATEGORY_KEYWORDS.items():
            if cat == "other":
                continue
            if any(kw in lower for kw in keywords):
                return cat
        return "other"

    @staticmethod
    def process_csv(csv_text: str) -> list[Transaction]:
        """Parse CSV text into Transaction objects with auto-categorization."""
        reader = csv.reader(io.StringIO(csv_text.strip()))
        rows = list(reader)
        if not rows:
            return []

        # Detect header
        header = [h.lower().strip() for h in rows[0]]
        has_header = any(h in header for h in ["date", "description", "amount"])
        data_rows = rows[1:] if has_header else rows

        transactions = []
        for i, row in enumerate(data_rows):
            if len(row) < 3:
                continue
            date = row[0].strip()
            description = row[1].strip()
            try:
                amount = float(row[2].strip().replace(",", ""))
            except ValueError:
                continue

            category = row[3].strip().lower() if len(row) > 3 and row[3].strip() else BudgetAgent.categorize(description)
            # Validate category
            if category not in CATEGORY_CONFIG:
                category = BudgetAgent.categorize(description)

            transactions.append(Transaction(
                id=f"csv-{i}-{int(datetime.now().timestamp() * 1000)}",
                date=date,
                description=description,
                amount=amount,
                category=category,
            ))

        return transactions


# ────────────────────────────────────────────
# Spending Analysis
# ────────────────────────────────────────────

def _analyze_impl(transactions: list[Transaction]) -> SpendingSummary:
    """Compute spending summary with stability scoring and personalized insight."""
    total_income = sum(t.amount for t in transactions if t.amount > 0)
    total_expenses = abs(sum(t.amount for t in transactions if t.amount < 0))
    net_savings = total_income - total_expenses
    savings_rate = round((net_savings / total_income * 100), 1) if total_income > 0 else 0

    # Safe-to-save: 80% of net savings (keep 20% buffer)
    safe_to_save = max(0, round(net_savings * 0.8))

    # Stability scoring based on expense-to-income ratio
    expense_ratio = total_expenses / total_income if total_income > 0 else 1.0
    if expense_ratio <= 0.55:
        stability_score = "stable"
    elif expense_ratio <= 0.75:
        stability_score = "moderate"
    else:
        stability_score = "volatile"

    # Category breakdown (expenses only)
    cat_totals: dict[str, float] = defaultdict(float)
    for t in transactions:
        if t.amount < 0:
            cat_totals[t.category] += abs(t.amount)

    breakdown = sorted(
        [
            CategoryBreakdown(
                category=cat,
                label=CATEGORY_CONFIG.get(cat, {}).get("label", cat),
                emoji=CATEGORY_CONFIG.get(cat, {}).get("emoji", "📦"),
                amount=amt,
                percentage=round(amt / total_expenses * 100, 1) if total_expenses > 0 else 0,
            )
            for cat, amt in cat_totals.items()
        ],
        key=lambda x: x.amount,
        reverse=True,
    )

    # Monthly trend
    month_data: dict[str, dict] = defaultdict(lambda: {"income": 0.0, "expenses": 0.0})
    for t in transactions:
        month_key = t.date[:7]  # YYYY-MM
        if t.amount > 0:
            month_data[month_key]["income"] += t.amount
        else:
            month_data[month_key]["expenses"] += abs(t.amount)

    trend = [
        MonthlyTrend(
            month=_format_month(m),
            income=data["income"],
            expenses=data["expenses"],
        )
        for m, data in sorted(month_data.items())
    ]

    # Personalized insight
    top_cat = breakdown[0] if breakdown else None
    if stability_score == "stable":
        insight = f"Your finances look healthy! You're saving {savings_rate}% of your income. "
        if top_cat:
            insight += f"Biggest spend: {top_cat.emoji} {top_cat.label} at ₹{top_cat.amount:,.0f}."
    elif stability_score == "moderate":
        insight = f"You're managing okay, but {round(expense_ratio * 100)}% of income goes to expenses. "
        if top_cat:
            insight += f"Consider optimizing {top_cat.emoji} {top_cat.label} (₹{top_cat.amount:,.0f})."
    else:
        insight = f"Expenses are high at {round(expense_ratio * 100)}% of income. "
        insight += "Consider keeping more liquid savings before locking into FDs."

    return SpendingSummary(
        total_income=total_income,
        total_expenses=total_expenses,
        net_savings=net_savings,
        safe_to_save=safe_to_save,
        savings_rate=savings_rate,
        stability_score=stability_score,
        category_breakdown=breakdown,
        monthly_trend=trend,
        insight=insight,
    )


def _format_month(ym: str) -> str:
    """Convert '2026-03' to 'Mar 26'."""
    try:
        dt = datetime.strptime(ym + "-01", "%Y-%m-%d")
        return dt.strftime("%b %y")
    except ValueError:
        return ym


# ─────────────────────────────────────────────────────────────────
# 3. FD Suggestion Agent
# ─────────────────────────────────────────────────────────────────

class FDSuggestionAgent:
    """Agent responsible for mapping user goal + surplus + time horizon to the optimal FD tenure and amount."""

    @staticmethod
    def generate_recommendation(summary: SpendingSummary) -> FDRecommendation | None:
        """Generate personalized FD recommendation based on spending analysis."""
        safe = summary.safe_to_save
        if safe < 5000:
            return None

        expense_ratio = summary.total_expenses / summary.total_income if summary.total_income > 0 else 1.0
        stability = summary.stability_score

        # ── Tenure selection logic ──
        if stability == "volatile":
            target_tenure = 6   # keep liquid
        elif stability == "moderate" or safe < 15000:
            target_tenure = 12
        elif safe < 30000:
            target_tenure = 24
        else:
            target_tenure = 36

        suggested_amount = (int(safe) // 1000) * 1000  # round down to nearest 1000

        # ── Find matching products ──
        def score_product(p: dict) -> tuple:
            has_tenure = target_tenure in p["tenure_options"]
            meets_min = suggested_amount >= p["min_amount"]
            return (has_tenure and meets_min, p["interest_rate"])

        eligible = sorted(FD_CATALOG, key=score_product, reverse=True)
        eligible = [p for p in eligible if suggested_amount >= p["min_amount"]]

        if not eligible:
            return None

        def build_fd_product(p: dict, tenure: int) -> FDProduct:
            # Find closest available tenure
            actual_tenure = tenure if tenure in p["tenure_options"] else min(
                p["tenure_options"], key=lambda t: abs(t - tenure)
            )
            tenure_label = _tenure_label(actual_tenure)
            maturity = _calc_maturity(suggested_amount, p["interest_rate"], actual_tenure)
            interest = maturity - suggested_amount

            tags = []
            if p["interest_rate"] >= 8.0:
                tags.append("High yield")
            if actual_tenure <= 12:
                tags.append("Quick access")
            if p["type"] == "NBFC":
                tags.append("NBFC")
            elif p["type"] == "HFC":
                tags.append("Housing Finance")
            tags.append("DICGC insured")

            return FDProduct(
                issuer=p["issuer"],
                type=p["type"],
                interest_rate=p["interest_rate"],
                min_amount=p["min_amount"],
                tenure_months=actual_tenure,
                tenure_label=tenure_label,
                lock_in_note=p["lock_in_note"],
                trust_context=p["trust_context"],
                maturity_amount=maturity,
                interest_earned=interest,
                tags=tags,
            )

        primary = build_fd_product(eligible[0], target_tenure)
        alternatives = [build_fd_product(p, target_tenure) for p in eligible[1:3]]

        # ── Build explanation ──
        top_expense = summary.category_breakdown[0] if summary.category_breakdown else None
        top_label = top_expense.label.lower() if top_expense else "general expenses"

        headline = _build_headline(stability, suggested_amount, primary)
        details = _build_details(summary, primary, top_label, stability)
        liquidity = _build_liquidity_note(stability, primary)

        return FDRecommendation(
            primary=primary,
            alternatives=alternatives,
            suggested_amount=suggested_amount,
            reason_headline=headline,
            reason_details=details,
            risk_level="low",
            liquidity_note=liquidity,
        )


# ─────────────────────────────────────────────────────────────────
# Agent Orchestrator (Router Hooks for FastAPI)
# ─────────────────────────────────────────────────────────────────
def parse_csv(csv_text: str) -> list[Transaction]:
    """Router hook that delegates to the Budget Agent."""
    return BudgetAgent.process_csv(csv_text)

def analyze(transactions: list[Transaction]) -> SpendingSummary:
    """Router hook that delegates to the spending analysis engine."""
    return _analyze_impl(transactions)

def recommend(summary: SpendingSummary) -> FDRecommendation | None:
    """Router hook that delegates to the FD Suggestion Agent."""
    return FDSuggestionAgent.generate_recommendation(summary)


def _tenure_label(months: int) -> str:
    if months < 12:
        return f"{months} months"
    years = months // 12
    remaining = months % 12
    if remaining:
        return f"{years} year{'s' if years > 1 else ''} {remaining} months"
    return f"{years} year{'s' if years > 1 else ''}"


def _calc_maturity(principal: int, annual_rate: float, tenure_months: int) -> int:
    """Quarterly compounding maturity calculation."""
    quarters = tenure_months / 3
    return round(principal * math.pow(1 + annual_rate / 400, quarters))


def _build_headline(stability: str, amount: int, fd: FDProduct) -> str:
    if stability == "volatile":
        return f"You can safely set aside ₹{amount:,} in a short {fd.tenure_label} FD while keeping the rest liquid."
    elif stability == "moderate":
        return f"You can safely save ₹{amount:,} this month in a {fd.tenure_label} FD at {fd.interest_rate}%."
    else:
        return f"Your spending is stable — invest ₹{amount:,} in a {fd.tenure_label} FD and earn ₹{fd.interest_earned:,} in interest."


def _build_details(summary: SpendingSummary, fd: FDProduct, top_expense: str, stability: str) -> list[str]:
    details = []

    # Line 1: spending context
    pct = round(summary.total_expenses / summary.total_income * 100) if summary.total_income > 0 else 0
    details.append(
        f"You spend about {pct}% of your income each month, mostly on {top_expense}. "
        f"That leaves ₹{summary.net_savings:,.0f} after expenses."
    )

    # Line 2: buffer logic
    buffer = summary.net_savings - summary.safe_to_save
    details.append(
        f"We're keeping ₹{buffer:,.0f} liquid as a safety buffer for unexpected expenses. "
        f"The remaining ₹{summary.safe_to_save:,.0f} is safe to invest."
    )

    # Line 3: tenure reasoning
    if stability == "volatile":
        details.append(
            f"Because your spending fluctuates, a short {fd.tenure_label} FD keeps your money accessible "
            f"while still earning {fd.interest_rate}% — much better than 3.5% in a savings account."
        )
    elif stability == "moderate":
        details.append(
            f"A {fd.tenure_label} tenure balances earning good interest ({fd.interest_rate}%) "
            f"with keeping your money reasonably accessible."
        )
    else:
        details.append(
            f"With stable spending, you can comfortably lock ₹{fd.maturity_amount - fd.interest_earned:,} "
            f"for {fd.tenure_label} and earn ₹{fd.interest_earned:,} in interest at {fd.interest_rate}%."
        )

    # Line 4: trust
    details.append(f"{fd.issuer} is {fd.trust_context}.")

    return details


def _build_liquidity_note(stability: str, fd: FDProduct) -> str:
    if stability == "volatile":
        return (
            f"This is a short-tenure FD on purpose. {fd.lock_in_note}. "
            "If something comes up, you can access your money relatively quickly."
        )
    return (
        f"{fd.lock_in_note}. Your remaining savings stay in your bank account "
        "for day-to-day needs and emergencies."
    )
