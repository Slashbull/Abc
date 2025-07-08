# alerts/top_picks.py
"""Weekly Top Picks Generator

Creates a snapshot of top N stocks by SmartScore and saves to CSV in snapshots dir.
"""
from __future__ import annotations

import pandas as pd
from config import SNAPSHOT_DIR, BUY_THRESHOLD

__all__ = ["generate_weekly_top_picks"]


def generate_weekly_top_picks(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Return top N stocks tagged BUY sorted by SmartScore and save to CSV."""
    buys = df[df["tag"] == '🟢 BUY']
    top = buys.nlargest(n, "smartscore")[
        ["ticker", "name", "current_price", "smartscore", "tag"]
    ].reset_index(drop=True)
    # Save snapshot
    filepath = SNAPSHOT_DIR / "weekly_top10.csv"
    top.to_csv(filepath, index=False)
    return top
