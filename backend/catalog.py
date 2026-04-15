"""FD Product Catalog — realistic issuers matching Blostem's multi-issuer model."""

FD_CATALOG = [
    {
        "issuer": "Bajaj Finance",
        "type": "NBFC",
        "interest_rate": 8.25,
        "min_amount": 15000,
        "tenure_options": [6, 12, 24, 36, 60],
        "lock_in_note": "Premature withdrawal allowed after 3 months with 1% penalty",
        "trust_context": "AAA-rated NBFC, 70,000+ Cr FD book, DICGC insured up to ₹5 lakh",
    },
    {
        "issuer": "Shriram Finance",
        "type": "NBFC",
        "interest_rate": 8.05,
        "min_amount": 10000,
        "tenure_options": [12, 24, 36, 60],
        "lock_in_note": "Premature withdrawal after 6 months with 0.5% penalty",
        "trust_context": "AA+ rated, 40+ years in financial services, DICGC insured",
    },
    {
        "issuer": "Mahindra Finance",
        "type": "NBFC",
        "interest_rate": 7.95,
        "min_amount": 5000,
        "tenure_options": [6, 12, 24, 36],
        "lock_in_note": "Premature withdrawal after 3 months, 1% penalty on rate",
        "trust_context": "AA+ rated, part of Mahindra Group, DICGC insured",
    },
    {
        "issuer": "PNB Housing Finance",
        "type": "HFC",
        "interest_rate": 7.75,
        "min_amount": 10000,
        "tenure_options": [12, 24, 36, 60],
        "lock_in_note": "Lock-in for first 12 months, then flexible withdrawal",
        "trust_context": "AA rated HFC, backed by PNB, DICGC insured",
    },
    {
        "issuer": "HDFC Ltd",
        "type": "HFC",
        "interest_rate": 7.40,
        "min_amount": 10000,
        "tenure_options": [12, 24, 36, 60],
        "lock_in_note": "Premature withdrawal after 3 months with 1% penalty",
        "trust_context": "AAA-rated, India's largest HFC, DICGC insured up to ₹5 lakh",
    },
    {
        "issuer": "Sundaram Finance",
        "type": "NBFC",
        "interest_rate": 7.85,
        "min_amount": 10000,
        "tenure_options": [12, 24, 36],
        "lock_in_note": "Premature withdrawal after 6 months, nominal penalty",
        "trust_context": "AAA-rated NBFC, 70+ year track record, DICGC insured",
    },
]

CATEGORY_CONFIG = {
    "income":        {"label": "Income",           "emoji": "💰"},
    "rent":          {"label": "Rent & Housing",    "emoji": "🏠"},
    "food":          {"label": "Food & Dining",     "emoji": "🍕"},
    "travel":        {"label": "Travel",            "emoji": "✈️"},
    "shopping":      {"label": "Shopping",          "emoji": "🛍️"},
    "bills":         {"label": "Bills & Utilities", "emoji": "📱"},
    "entertainment": {"label": "Entertainment",     "emoji": "🎬"},
    "health":        {"label": "Health",            "emoji": "💊"},
    "education":     {"label": "Education",         "emoji": "📚"},
    "other":         {"label": "Other",             "emoji": "📦"},
}

# Keywords for auto-categorization
CATEGORY_KEYWORDS = {
    "income": ["salary", "credit", "freelance", "payment received", "refund", "bonus", "interest earned"],
    "rent": ["rent", "housing", "maintenance", "society", "pg ", "hostel"],
    "food": [
        "swiggy", "zomato", "food", "grocery", "bigbasket", "dmart", "d-mart",
        "restaurant", "cafe", "blinkit", "zepto", "dunzo", "dining",
    ],
    "travel": [
        "uber", "ola", "rapido", "fuel", "petrol", "diesel", "metro", "bus",
        "train", "flight", "irctc", "airline", "cab",
    ],
    "shopping": [
        "amazon", "flipkart", "myntra", "ajio", "nykaa", "meesho", "purchase",
        "mall", "store",
    ],
    "bills": [
        "electricity", "electric", "bill", "recharge", "mobile", "internet",
        "broadband", "gas cylinder", "water bill", "dth", "insurance premium",
    ],
    "entertainment": [
        "netflix", "spotify", "hotstar", "prime video", "movie", "pvr", "inox",
        "gaming", "subscription",
    ],
    "health": ["pharmacy", "apollo", "doctor", "hospital", "medicine", "lab test", "health"],
    "education": ["coursera", "udemy", "book", "course", "tuition", "school", "college"],
    "other": [],
}
