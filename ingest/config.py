# config.py
"""
Global configuration for M.A.N.T.R.A.

Contains constants and settings for the entire system.
No I/O or heavy logic here—only pure values.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Final

# ────────────────────────────────────────────────────────────────
# 🔗  Google-Sheet URL  →  CSV export
# ────────────────────────────────────────────────────────────────
GOOGLE_SHEET_URL: Final[str] = os.getenv(
    "SHEET_URL",
    "https://docs.google.com/spreadsheets/d/1XipQ2_Cap60A9tfxDmmaXInsz_xFE42VtwVIQyUL-Hs/edit?usp=sharing",
).strip()

CSV_EXPORT_URL: Final[str] = GOOGLE_SHEET_URL.replace(
    "/edit?usp=sharing",
    "/gviz/tq?tqx=out:csv",
)

# ────────────────────────────────────────────────────────────────
# 🧠  SmartScore Weights (0–100 composite)
# ────────────────────────────────────────────────────────────────
SMART_WEIGHTS: Final[dict[str, int]] = {
    "momentum":     25,
    "value":        20,
    "volume":       20,
    "timing":       15,
    "confirmation": 10,
    "buy_zone":     10,
}

BUY_THRESHOLD:   Final[int] = 80
WATCH_THRESHOLD: Final[int] = 60

# ────────────────────────────────────────────────────────────────
# 📂  Project Paths
# ────────────────────────────────────────────────────────────────
ROOT: Final[Path] = Path(__file__).resolve().parent
SNAPSHOT_DIR: Final[Path] = ROOT / "snapshots"
SNAPSHOT_DIR.mkdir(exist_ok=True)

# ────────────────────────────────────────────────────────────────
# 🎨  UI constants
# ────────────────────────────────────────────────────────────────
APP_TITLE: Final[str] = "📈 M.A.N.T.R.A – Advanced Stock Dashboard"

LIGHT_THEME: Final[dict[str, str]] = {
    "primaryColor":             "#2962FF",
    "backgroundColor":          "#FFFFFF",
    "secondaryBackgroundColor": "#F5F5F5",
    "textColor":                "#212121",
}

DISCOVER_TIERS: Final[list[str]] = ["100 ↓", "100↑", "200 ↑", "500 ↑", "1K ↑", "2K ↑", "5K ↑"]
EPS_TIERS:      Final[list[str]] = ["5↓", "5↑", "15↑", "35↑", "55↑", "75↑", "95↑"]

__all__ = [
    "CSV_EXPORT_URL",
    "SMART_WEIGHTS",
    "BUY_THRESHOLD",
    "WATCH_THRESHOLD",
    "SNAPSHOT_DIR",
    "APP_TITLE",
    "LIGHT_THEME",
    "DISCOVER_TIERS",
    "EPS_TIERS",
]
