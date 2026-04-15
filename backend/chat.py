"""
AI Chat responder — plain-English financial explanations.
Structured responses grounded in the user's actual data.
"""

from models import SpendingSummary, FDRecommendation
from catalog import CATEGORY_CONFIG


class FinanceTutorAgent:
    """
    Explains financial concepts natively in conversational language.
    (This class stubs the planned RAG vector implementation outlined in the MVP System Design).
    """
    @staticmethod
    def converse(question: str, summary: SpendingSummary | None, recommendation: FDRecommendation | None) -> str:
        q = question.lower().strip()

        # ── What is an FD ──
        if "what is" in q and ("fd" in q or "fixed deposit" in q):
            return _explain_fd()

        # ── Why this recommendation ──
        if "why" in q and any(w in q for w in ["recommend", "suggesting", "this fd", "this"]):
            return _explain_recommendation(summary, recommendation)

        # ── Can I save X ──
        if "can i" in q and "save" in q:
            return _check_savings(q, summary)

        # ── Savings account vs FD ──
        if "savings" in q and any(w in q for w in ["why not", "instead", "vs", "versus", "better"]):
            return _compare_savings_fd(summary)

        # ── Spending summary ──
        if any(w in q for w in ["summary", "spending", "overview", "breakdown"]):
            return _spending_summary(summary)

        # ── Emergency fund ──
        if "emergency" in q:
            return _emergency_fund(summary)

        # ── How much to invest ──
        if any(w in q for w in ["how much", "invest", "put in"]):
            return _how_much(summary, recommendation)

        # ── Greeting ──
        if any(w in q for w in ["hello", "hi", "hey"]) or len(q) < 10:
            return _greeting()

        # ── Catch-all ──
        return _fallback()


# ─────────────────────────────────────────────────────────────────
# Agent Orchestrator (Router Hook)
# ─────────────────────────────────────────────────────────────────
def respond(question: str, summary: SpendingSummary | None, recommendation: FDRecommendation | None) -> str:
    """Router hook that delegates the user's question to the Finance Tutor Agent."""
    return FinanceTutorAgent.converse(question, summary, recommendation)


def _explain_fd() -> str:
    return (
        "**A Fixed Deposit (FD)** is one of the safest ways to grow your money 🏦\n\n"
        "Here's how it works:\n"
        "- You deposit a lump sum with a bank or NBFC\n"
        "- The money earns a **fixed interest rate** (typically 7-8.5% per year)\n"
        "- After the agreed period (tenure), you get back your money + interest\n\n"
        "**Why it's great for beginners:**\n"
        "- ✅ Guaranteed returns — no market risk\n"
        "- ✅ Deposits up to ₹5 lakh are insured by DICGC\n"
        "- ✅ Higher interest than savings accounts (3.5-4%)\n"
        "- ✅ You can choose tenures from 6 months to 5 years\n\n"
        "Think of it as putting your money in a \"safe locker\" that pays you rent for keeping it there! 🔐"
    )


def _explain_recommendation(summary: SpendingSummary | None, rec: FDRecommendation | None) -> str:
    if not rec or not summary:
        return "I haven't made a recommendation yet. Upload your transactions first and I'll analyze your spending to suggest the best FD for you! 📊"

    lines = [f"**Why I'm recommending this FD** 🎯\n"]
    for detail in rec.reason_details:
        lines.append(f"- {detail}")
    lines.append(f"\n**Liquidity:** {rec.liquidity_note}")
    lines.append(f"\n**Bottom line:** Your money earns ₹{rec.primary.interest_earned:,.0f} in interest instead of sitting idle in savings. That's real money! 💰")
    return "\n".join(lines)


def _check_savings(question: str, summary: SpendingSummary | None) -> str:
    if not summary:
        return "I need to see your transactions first! Upload a CSV or add some expenses, and I'll calculate exactly how much you can safely save. 📋"

    # Try to extract amount from question
    import re
    match = re.search(r"(\d[\d,]*)", question)
    target = int(match.group(1).replace(",", "")) if match else int(summary.safe_to_save)

    if target <= summary.safe_to_save:
        return (
            f"**Yes, you can safely save ₹{target:,} this month!** ✅\n\n"
            f"After all your expenses (₹{summary.total_expenses:,.0f}), you have ₹{summary.net_savings:,.0f} left over. "
            f"I've kept a 20% buffer for unexpected expenses, so ₹{summary.safe_to_save:,.0f} is your safe-to-save amount.\n\n"
            f"₹{target:,} is well within that range — go for it! 🎯"
        )
    else:
        return (
            f"**₹{target:,} is a stretch this month.** ⚠️\n\n"
            f"Your safe-to-save amount is ₹{summary.safe_to_save:,.0f}. "
            f"Saving ₹{target:,} would eat into your safety buffer.\n\n"
            f"**My suggestion:** Start with ₹{summary.safe_to_save:,.0f} and increase gradually. "
            f"Consistency beats intensity! 📈"
        )


def _compare_savings_fd(summary: SpendingSummary | None) -> str:
    example_amount = int(summary.safe_to_save) if summary and summary.safe_to_save >= 5000 else 20000
    savings_interest = round(example_amount * 0.035)
    fd_interest = round(example_amount * 0.0825)

    return (
        f"**Savings account vs FD — the math is simple:**\n\n"
        f"| | Savings Account | Fixed Deposit |\n"
        f"|---|---|---|\n"
        f"| Interest rate | 3-4% | 7-8.5% |\n"
        f"| ₹{example_amount:,} for 1 year | ₹{savings_interest:,} earned | ₹{fd_interest:,} earned |\n"
        f"| Risk | Zero | Zero |\n"
        f"| Lock-in | None | Yes (but can break early) |\n\n"
        f"Keeping ALL your money in savings means **inflation eats your purchasing power**. "
        f"Prices rise ~6% per year, but savings only earns ~3.5%.\n\n"
        f"The smart approach:\n"
        f"- Keep 2-3 months expenses in savings (for emergencies)\n"
        f"- Put the rest in FDs (earn 2x more interest)\n"
        f"- You can always break an FD early if needed (small penalty)\n\n"
        f"You're literally leaving money on the table by not having an FD! 💸"
    )


def _spending_summary(summary: SpendingSummary | None) -> str:
    if not summary:
        return "I don't have your transaction data yet. Upload a CSV or enter expenses manually, and I'll give you a complete spending breakdown! 📊"

    top_cats = "\n".join(
        f"- {c.emoji} {c.label}: ₹{c.amount:,.0f} ({c.percentage}%)"
        for c in summary.category_breakdown[:4]
    )

    health = "You're in good shape!" if summary.stability_score == "stable" else "Room for improvement."

    return (
        f"**Your Monthly Summary 📊**\n\n"
        f"💰 **Income:** ₹{summary.total_income:,.0f}\n"
        f"💸 **Expenses:** ₹{summary.total_expenses:,.0f}\n"
        f"✅ **Net savings:** ₹{summary.net_savings:,.0f}\n"
        f"🎯 **Safe to save:** ₹{summary.safe_to_save:,.0f}\n"
        f"📈 **Savings rate:** {summary.savings_rate}%\n"
        f"🔒 **Stability:** {summary.stability_score.title()}\n\n"
        f"**Top spending categories:**\n{top_cats}\n\n"
        f"**{summary.insight}** {health} 💪"
    )


def _emergency_fund(summary: SpendingSummary | None) -> str:
    if summary:
        min_fund = int(summary.total_expenses * 3)
        ideal_fund = int(summary.total_expenses * 6)
        expense_str = f"\n\nBased on your spending (₹{summary.total_expenses:,.0f}/month):\n- **Minimum:** ₹{min_fund:,}\n- **Ideal:** ₹{ideal_fund:,}"
    else:
        expense_str = "\n\nUpload your transactions and I'll calculate the exact amount."

    return (
        f"**Building an emergency fund is your #1 priority** 🛡️\n\n"
        f"You should have **3-6 months of expenses** saved.{expense_str}\n\n"
        f"**Where to keep it:**\n"
        f"1. **1 month** in savings account (instant access)\n"
        f"2. **2-5 months** in short-tenure FDs (6-12 months)\n"
        f"   - Earns better interest\n"
        f"   - Can break early if truly needed\n\n"
        f"This way your safety net also earns for you! 🎯"
    )


def _how_much(summary: SpendingSummary | None, rec: FDRecommendation | None) -> str:
    if not summary:
        return "Upload your transactions first, and I'll calculate the ideal amount based on your actual spending patterns. 📋"

    if rec:
        return (
            f"Based on your spending, **₹{rec.suggested_amount:,}** is a great starting point.\n\n"
            f"Here's my logic:\n"
            f"- Your monthly income: ₹{summary.total_income:,.0f}\n"
            f"- Your monthly expenses: ₹{summary.total_expenses:,.0f}\n"
            f"- Net savings: ₹{summary.net_savings:,.0f}\n"
            f"- After keeping 20% buffer: **₹{summary.safe_to_save:,.0f} safe to invest**\n\n"
            f"I rounded down to ₹{rec.suggested_amount:,} to keep numbers clean. "
            f"At {rec.primary.interest_rate}%, you'd earn ₹{rec.primary.interest_earned:,} "
            f"over {rec.primary.tenure_label}. 💰"
        )

    return (
        f"Your safe-to-save amount is **₹{summary.safe_to_save:,.0f}**.\n\n"
        f"I'd suggest starting with ₹{(int(summary.safe_to_save) // 1000) * 1000:,} "
        f"in a 12-month FD to build the habit. You can always increase next month!"
    )


def _greeting() -> str:
    return (
        "Hey there! 👋 I'm your AI money coach.\n\n"
        "I can help you with:\n"
        "- 📊 **Understanding your spending** — \"Show me my summary\"\n"
        "- 💰 **Savings advice** — \"Can I save ₹5000 this month?\"\n"
        "- 🏦 **FD guidance** — \"What is an FD?\" or \"Why are you recommending this?\"\n"
        "- 🛡️ **Emergency funds** — \"How much emergency fund do I need?\"\n"
        "- 📈 **Savings vs FD** — \"Why not keep money in savings?\"\n\n"
        "What would you like to know?"
    )


def _fallback() -> str:
    return (
        "That's a great question! 🤔\n\n"
        "Here's what I can help with right now:\n\n"
        "1. **\"What is an FD?\"** — Fixed deposits explained simply\n"
        "2. **\"Why this recommendation?\"** — My reasoning, step by step\n"
        "3. **\"Can I save ₹X this month?\"** — I'll check your numbers\n"
        "4. **\"Show my summary\"** — Full spending breakdown\n"
        "5. **\"Why not savings account?\"** — FD vs savings math\n"
        "6. **\"How much should I invest?\"** — Personalized amount\n\n"
        "Try asking one of these! 🚀"
    )
