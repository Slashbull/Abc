# ingest/ingest.py
"""M.A.N.T.R.A. · INTAKE LAYER

Pure I/O: download the two Google‑Sheets tabs (Watchlist + Industry Analysis)
into raw *pandas* DataFrames.

* No cleaning, no parsing – downstream modules handle that.
* Caches each CSV in‑memory for 30 minutes via ``st.cache_data`` if running
  inside Streamlit; otherwise falls back to ``functools.lru_cache``.
"""
from __future__ import annotations

import os
from functools import lru_cache
from typing import Final, Callable

import pandas as pd

# ---------------------------------------------------------------------------
# 🔗 Google‑Sheet endpoints
# ---------------------------------------------------------------------------

# One spreadsheet, two tabs.  Replace GIDs below if your sheet uses different IDs.
SPREADSHEET_ID: Final[str] = os.getenv(
    "MANTA_SHEET_ID", "1XipQ2_Cap60A9tfxDmmaXInsz_xFE42VtwVIQyUL-Hs"
)

WATCHLIST_GID: Final[str] = os.getenv("WATCHLIST_GID", "0")            # tab "Watchlist"
INDUSTRY_GID: Final[str] = os.getenv("INDUSTRY_GID", "842039302")      # tab "Industry Analysis"

_BASE = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv&gid={{gid}}"


def _csv_url(gid: str) -> str:
    """Return a direct‑CSV export URL for the given *gid* tab."""
    return _BASE.format(gid=gid)


# ---------------------------------------------------------------------------
# 🧰 Caching helper – works with or without Streamlit.
# ---------------------------------------------------------------------------

def _cache(func: Callable[..., pd.DataFrame]) -> Callable[..., pd.DataFrame]:
    """Wrap *func* in either Streamlit or LRU cache depending on runtime."""

    try:
        import streamlit as st  # noqa: WPS433 (dynamic import only once here)

        return st.cache_data(ttl=1800)(func)  # 30‑minute shared cache

    except ModuleNotFoundError:  # running in plain Python (tests, CLI)
        return lru_cache(maxsize=2)(func)


# ---------------------------------------------------------------------------
# 🚚 Public ingestion functions
# ---------------------------------------------------------------------------

@_cache
def fetch_watchlist_raw(skip_metadata_rows: int = 3) -> pd.DataFrame:  # noqa: WPS110 (reasonable argname)
    """Download **Watchlist** tab and return raw DataFrame.

    Google exports UTF‑8 CSV, so *pandas* can ingest directly.  We skip the
    first three rows because your sheet stores header comments above the real
    column names (row 4 = actual header line).
    """
    url = _csv_url(WATCHLIST_GID)
    return pd.read_csv(url, skiprows=skip_metadata_rows)


@_cache
def fetch_industry_raw(skip_metadata_rows: int = 3) -> pd.DataFrame:  # noqa: WPS110
    """Download **Industry Analysis** tab and return raw DataFrame."""
    url = _csv_url(INDUSTRY_GID)
    return pd.read_csv(url, skiprows=skip_metadata_rows)


# ---------------------------------------------------------------------------
# 🏁 Convenience wrapper for downstream pipeline
# ---------------------------------------------------------------------------

def get_raw_frames() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return *(watchlist_df, industry_df)* in one call."""
    return fetch_watchlist_raw(), fetch_industry_raw()


__all__ = [
    "fetch_watchlist_raw",
    "fetch_industry_raw",
    "get_raw_frames",
]
