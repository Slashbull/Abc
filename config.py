# config.py
import os
from dotenv import load_dotenv

# Load .env variables if present
load_dotenv()

# =============================================================================
# 🔐 Authentication (optional for login-based apps)
# =============================================================================
USERNAME = os.getenv("APP_USERNAME", "admin")
PASSWORD = os.getenv("APP_PASSWORD", "admin123")

# =============================================================================
# 📊 Google Sheet Config
# =============================================================================
GOOGLE_SHEET_EDITABLE_LINK = os.getenv(
    "GOOGLE_SHEET_EDITABLE_LINK",
    "https://docs.google.com/spreadsheets/d/1XipQ2_Cap60A9tfxDmmaXInsz_xFE42VtwVIQyUL-Hs/edit?usp=sharing"
).strip()

# Convert to exportable CSV URL
GOOGLE_SHEET_CSV_URL = GOOGLE_SHEET_EDITABLE_LINK.replace("/edit?usp=sharing", "/gviz/tq?tqx=out:csv")

DEFAULT_SHEET_NAME = os.getenv("DEFAULT_SHEET_NAME", "Watchlist")

# =============================================================================
# 🧠 Scoring Logic Config (Weights can be adjusted anytime)
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

# Score thresholds for tags
BUY_SCORE_THRESHOLD = 75
WATCHLIST_SCORE_THRESHOLD = 60

# Tag Labels
TAG_BUY = "🟢 BUY"
TAG_WATCH = "🟡 WATCH"
TAG_AVOID = "🔴 AVOID"

# =============================================================================
# 🔧 App Settings
# =============================================================================
APP_TITLE = "📈 M.A.N.T.R.A. – Stock Intelligence Dashboard"
APP_VERSION = "v1.0.0"
APP_AUTHOR = "Wasim K"

# =============================================================================
# 🧠 System Config
# =============================================================================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")  # DEBUG, INFO, WARNING, ERROR
CACHE_MAX_ENTRIES = int(os.getenv("CACHE_MAX_ENTRIES", 100))

# =============================================================================
# 🎯 Column Constants (can be used across logic files)
# =============================================================================
COL_EPS_CHANGE = "EPS (% Change)"
COL_PE = "PE"
COL_PRICE = "Current Price"
COL_200DMA = "200 Day Avg"
COL_RVOL = "RVOL"
COL_RETURN_1Y = "1 Year"
COL_SECTOR = "Sector"
COL_TAG = "Tag"
