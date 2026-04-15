"""Pydantic models for request/response validation."""

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from typing import Literal, Optional

class CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

Category = Literal[
    "income", "rent", "food", "travel", "shopping",
    "bills", "entertainment", "health", "education", "other"
]


class Transaction(CamelModel):
    id: str
    date: str
    description: str
    amount: float  # negative = expense, positive = income
    category: Category


class CategoryBreakdown(CamelModel):
    category: Category
    label: str
    emoji: str
    amount: float
    percentage: float


class MonthlyTrend(CamelModel):
    month: str
    income: float
    expenses: float


class SpendingSummary(CamelModel):
    total_income: float
    total_expenses: float
    net_savings: float
    safe_to_save: float
    savings_rate: float  # percentage
    stability_score: str  # "stable", "moderate", "volatile"
    category_breakdown: list[CategoryBreakdown]
    monthly_trend: list[MonthlyTrend]
    insight: str  # one-line personalized insight


class FDProduct(CamelModel):
    issuer: str
    type: str  # "NBFC", "HFC", "Bank"
    interest_rate: float
    min_amount: int
    tenure_months: int
    tenure_label: str
    lock_in_note: str
    trust_context: str
    maturity_amount: float
    interest_earned: float
    tags: list[str]


class FDRecommendation(CamelModel):
    primary: FDProduct
    alternatives: list[FDProduct]
    suggested_amount: int
    reason_headline: str
    reason_details: list[str]
    risk_level: str
    liquidity_note: str


class AnalyzeRequest(CamelModel):
    transactions: list[Transaction]


class ChatRequest(CamelModel):
    message: str
    summary: Optional[SpendingSummary] = None
    recommendation: Optional[FDRecommendation] = None


class ChatResponse(CamelModel):
    reply: str
