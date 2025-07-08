# clean/clean.py
"""M.A.N.T.R.A. · CLEAN LAYER

Transforms raw CSV data (downloaded via *ingest/ingest.py*) into a tidy,
analysis‑ready DataFrame.  This is the **only** place that mutates the data
structure.  All downstream code assumes these canonical column names & dtypes.
"""
from __future__ import annotations

import re
from typing import Final

import pandas as pd

__all__ = [
    "clean_watchlist",
    "clean_industry",
]

# ---------------------------------------------------------------------------
# 🔤 Column Normalisation
# ---------------------------------------------------------------------------

WHITESPACE_RE: Final[re.Pattern[str]] = re.compile(r"\s+")
PERCENT_RE: Final[re.Pattern[str]] = re.compile(r"[%]$")
ARROW_RE: Final[re.Pattern[str]] = re.compile(r"[▲▼]")
RUPEE_RE: Final[re.Pattern[str]] = re.compile(r"₹")
COMMA_RE: Final[re.Pattern[str]] = re.compile(r",")


_NUMERIC_SUFFIXES: Final[list[str]] = [
    "Current Price",
    "52 Week LOW",
    "52 Week HIGH",
    "% From Low",
    "% From High",
    "20 Day Avg",
    "50 Day Avg",
    "200 Day Avg",
    "1 Day Change",
    "3 Days Returns",
    "7 Days Returns",
    "30 Days Returns",
    "3 Months",
    "6 Months",
    "1 Year",
    "3 Year",
    "5 Year",
    "Volume",
    "7 Days Volume",
    "30 Days Volume",
    "3 Months Volume",
    "1-day vs. 90-day",
    "7-day vs. 90-day",
    "30-day vs. 90-day",
    "RVOL",
    "Prev Close",
    "PE",
    "EPS (Current)",
    "EPS (Last Qtr)",
    "EPS (TTM)",
    "EPS (% Change)",
]


def _snake_case(col: str) -> str:  # noqa: WPS110 (col ok)
    """Convert *col* to snake_case safe for Python access."""
    col = WHITESPACE_RE.sub("_", col.strip())
    col = col.replace("/", "_").replace("%", "Pct")
    col = col.replace("(", "").replace(")", "")
    col = col.replace("↓", "").replace("↑", "")
    return re.sub(r"__+", "_", col)


# ---------------------------------------------------------------------------
# 🚿 Cleaning helpers
# ---------------------------------------------------------------------------

def _coerce_numeric(series: pd.Series) -> pd.Series:  # noqa: D401
    """Strip ₹, arrows, commas, percent then convert to float."""
    cleaned = (
        series.astype(str)
        .pipe(RUPEE_RE.sub, "")
        .pipe(ARROW_RE.sub, "")
        .pipe(COMMA_RE.sub, "")
        .pipe(PERCENT_RE.sub, "")
        .str.strip()
        .replace({"": pd.NA, "-": pd.NA})
    )
    return pd.to_numeric(cleaned, errors="coerce")


# ---------------------------------------------------------------------------
# 🧹 Public cleaners
# ---------------------------------------------------------------------------

def clean_watchlist(raw: pd.DataFrame) -> pd.DataFrame:  # noqa: WPS231 (acceptable length)
    """Return a tidy Watchlist DataFrame ready for signal engines."""
    df = raw.copy()

    # 1️⃣ Drop unnamed garbage columns
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    # 2️⃣ Standardise header names → snake_case
    df.columns = [_snake_case(c) for c in df.columns]

    # 3️⃣ Ensure ticker column exists + drop empties
    if "enter_ticker" in df.columns:
        df.rename(columns={"enter_ticker": "ticker"}, inplace=True)
    df.dropna(subset=["ticker"], inplace=True)

    # 4️⃣ Numeric coercion for all numeric‑intended columns
    for col in _NUMERIC_SUFFIXES:
        snake = _snake_case(col)
        if snake in df.columns:
            df[snake] = _coerce_numeric(df[snake])

    return df.reset_index(drop=True)


def clean_industry(raw: pd.DataFrame) -> pd.DataFrame:
    """Return a tidy Industry‑Analysis DataFrame."""
    df = raw.copy()
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    df.columns = [_snake_case(c) for c in df.columns]
    df.dropna(subset=[df.columns[0]], inplace=True)  # keep rows with ticker/sector

    # Coerce all return % columns to numeric
    pct_cols = [c for c in df.columns if c.endswith("%") or "Pct" in c]
    for col in pct_cols:
        df[col] = _coerce_numeric(df[col])

    return df.reset_index(drop=True)
