# ingest/ingest.py
"""
INGEST MODULE

Fetches CSV exports of Watchlist and Industry Analysis tabs from Google Sheets.
Uses caching to avoid redundant network calls.
"""
from __future__ import annotations

import os
from functools import lru_cache
from typing import Final

import pandas as pd

from config import CSV_EXPORT_URL

# Override GIDs for specific tabs
SPREADSHEET_ID: Final[str] = os.getenv(
    "SHEET_ID",
    CSV_EXPORT_URL.split("/d/")[1].split("/")[0]
)
WATCHLIST_GID: Final[str] = os.getenv("WATCHLIST_GID", "0")
INDUSTRY_GID: Final[str] = os.getenv("INDUSTRY_GID", "842039302")

_BASE_URL: Final[str] = (
    f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv&gid={{gid}}"
)


def _sheet_url(gid: str) -> str:
    return _BASE_URL.format(gid=gid)


@lru_cache(maxsize=2)
def fetch_watchlist_raw(skiprows: int = 3) -> pd.DataFrame:
    """Fetch raw Watchlist CSV and return DataFrame."""
    url = _sheet_url(WATCHLIST_GID)
    df = pd.read_csv(url, skiprows=skiprows)
    return df


@lru_cache(maxsize=2)
def fetch_industry_raw(skiprows: int = 3) -> pd.DataFrame:
    """Fetch raw Industry Analysis CSV and return DataFrame."""
    url = _sheet_url(INDUSTRY_GID)
    df = pd.read_csv(url, skiprows=skiprows)
    return df


def get_raw_frames() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return watchlist, industry raw DataFrames."""
    return fetch_watchlist_raw(), fetch_industry_raw()

__all__ = ["get_raw_frames", "fetch_watchlist_raw", "fetch_industry_raw"]
