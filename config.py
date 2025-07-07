# config.py

# === Google Sheet Settings ===
GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1XipQ2_Cap60A9tfxDmmaXInsz_xFE42VtwVIQyUL-Hs/export?format=csv&gid=0"  # GID for Watchlist sheet

# === Scoring Weights ===
SCORING_WEIGHTS = {
    "EPS_Change": 20,
    "Low_PE": 15,
    "Under_200DMA": 10,
    "Close_to_Buy_Target": 10,
    "RVOL_High": 15,
    "High_Returns_1Y": 20,
    "Momentum_Sector": 10
}

# === Thresholds ===
BUY_SCORE_THRESHOLD = 75
WATCHLIST_SCORE_THRESHOLD = 60

# === App Title ===
APP_TITLE = "M.A.N.T.R.A. | Smart Stock Dashboard"
