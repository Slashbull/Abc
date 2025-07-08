# clean/clean.py
"""CLEAN MODULE

Transforms raw DataFrames into tidy, analysis-ready DataFrames with
consistent snake_case columns and numeric types.
"""
from __future__ import annotations

import re
from typing import Final

import pandas as pd

__all__ = ["clean_watchlist", "clean_industry"]

# Regex patterns
_WHITESPACE_RE: Final[re.Pattern[str]] = re.compile(r"\s+")
_CLEAN_REPLACEMENTS: Final[dict[str, str]] = {
    r"[%]": "Pct",
    r"[()\n]": "",
    r"[↓↑]": "",
    r"/": "_",
}

# Numeric columns to coerce (pre-snake-case)
_NUMERIC_COLS_ORIG: Final[list[str]] = [
    "Current Price", "1 Day Change", "52 Week LOW", "52 Week HIGH",
    "% From Low", "% From High", "20 Day Avg", "50 Day Avg", "200 Day Avg",
    "3 Days Returns", "7 Days Returns", "30 Days Returns", "3 Months",
    "6 Months", "1 Year", "3 Year", "5 Year", "Volume", "7 Days Volume",
    "30 Days Volume", "3 Months Volume", "1-day vs. 90-day",
    "7-day vs. 90-day", "30-day vs. 90-day", "RVOL", "Prev Close",
    "PE", "EPS (Current)", "EPS (Last Qtr)", "EPS (TTM)", "EPS (% Change)",
]


def _snake_case(col: str) -> str:
    """Convert string to snake_case"""
    s = col.strip()
    # Apply replacements
    for pat, repl in _CLEAN_REPLACEMENTS.items():
        s = re.sub(pat, repl, s)
    # Normalize whitespace to underscore
    s = _WHITESPACE_RE.sub("_", s)
    # Lowercase
    return s.lower()


def _coerce_numeric(series: pd.Series) -> pd.Series:
    """Strip symbols and convert to float."""
    # Remove rupee, commas, percent signs, arrows
    s = series.astype(str)
    s = s.str.replace(r"₹", "", regex=False)
    s = s.str.replace(r",", "", regex=False)
    s = s.str.replace(r"%", "", regex=False)
    s = s.str.replace(r"▲", "", regex=False)
    s = s.str.replace(r"▼", "-", regex=False)
    s = s.str.strip()
    return pd.to_numeric(s, errors="coerce")


def clean_watchlist(raw: pd.DataFrame) -> pd.DataFrame:
    """Clean raw watchlist DataFrame."""
    df = raw.copy()
    # Drop unnamed
    df = df.loc[:, ~df.columns.str.contains(r"^Unnamed")]  # type: ignore
    # Snake-case headers
    df.columns = [_snake_case(c) for c in df.columns]
    # Rename ticker column if exists
    if "enter_ticker" in df.columns:
        df.rename(columns={"enter_ticker": "ticker"}, inplace=True)
    # Drop rows missing ticker
    df.dropna(subset=["ticker"], inplace=True)
    # Coerce numeric columns
    for orig in _NUMERIC_COLS_ORIG:
        col = _snake_case(orig)
        if col in df.columns:
            df[col] = _coerce_numeric(df[col])
    return df.reset_index(drop=True)


def clean_industry(raw: pd.DataFrame) -> pd.DataFrame:
    """Clean raw industry DataFrame."""
    df = raw.copy()
    df = df.loc[:, ~df.columns.str.contains(r"^Unnamed")]  # type: ignore
    df.columns = [_snake_case(c) for c in df.columns]
    # Drop blank rows
    first_col = df.columns[0]
    df.dropna(subset=[first_col], inplace=True)
    # Coerce any column with pct or returning numeric
    for col in df.columns:
        if any(key in col for key in ["pct", "day", "year", "return"]):
            df[col] = _coerce_numeric(df[col])
    return df.reset_index(drop=True)
