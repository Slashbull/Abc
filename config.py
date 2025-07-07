# config.py

import os
from dotenv import load_dotenv

# Load .env variables if present
load_dotenv()

# =============================================================================
# 🔐 Authentication (Optional: Only if you want app login)
# =============================================================================
USERNAME = os.getenv("APP_USERNAME", "admin")
PASSWORD = os.getenv("APP_PASSWORD", "admin123")

# =============================================================================
# 📊 Google Sheet Configuration
# =============================================================================
GOOGLE_SHEET_EDITABLE_LINK = os.getenv(
    "GOOGLE_SHEET_EDITABLE_LINK",
    "https://docs.google.com/spreadsheets/d/1XipQ2_Cap60A9tfxDmmaXInsz_xFE42VtwVIQyUL-Hs/edit?usp=sharing"
).strip()

# Convert to exportable CSV URL for direct loading
if "/edit" in GOOGLE_SHEET_EDITABLE_LINK:
    GOOGLE_SHEET_CSV_URL = GOOGLE_SHEET_EDITABLE_LINK.replace("/edit?usp=sharing", "/gviz/tq?tqx=out:csv")
else:
    GOOGLE_SHEET_CSV_URL = GOOGLE_SHEET_EDITABLE_LINK

DEFAULT_SHEET_NAME = os.getenv("DEFAULT_SHEET_NAME", "Watchlist")

# =============================================================================
# 🧠 Scoring Logic Configuration (weights for the MANTRA system)
# =============================================================================
SCORING_WEIGHTS = {
    "EPS_Change": 20,
    "Low_PE": 15,
    "Under_200DMA": 10,
    "Close_to_Buy_Target": 10,
    "RVOL_High": 15,
    "High_Returns_1Y": 20,
    "Momentum_Sector": 10,
}

BUY_SCORE_THRESHOLD = 75
WATCHLIST_SCORE_THRESHOLD = 60

TAG_BUY = "🟢 BUY"
TAG_WATCH = "🟡 WATCH"
TAG_AVOID = "🔴 AVOID"

# =============================================================================
# ⚙️ App Info
# =============================================================================
APP_TITLE = "📈 M.A.N.T.R.A. – Stock Intelligence Dashboard"
APP_VERSION = "v1.0.0"
APP_AUTHOR = "Wasim K"

# =============================================================================
# 🔧 System Configuration
# =============================================================================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")  # DEBUG, INFO, WARNING, ERROR
CACHE_MAX_ENTRIES = int(os.getenv("CACHE_MAX_ENTRIES", 100))

# =============================================================================
# 🏷️ Column Constants (used across all modules for reliability)
# =============================================================================
COL_TICKER = "Ticker"
COL_NAME = "Name"
COL_PE = "PE"
COL_PRICE = "Current_Price"
COL_200DMA = "200_Day_Avg"
COL_RVOL = "RVOL"
COL_RETURN_1Y = "1_Year"
COL_EPS_CHANGE = "EPS_Pct_Change"
COL_SECTOR = "Sector"
COL_TAG = "Tag"
