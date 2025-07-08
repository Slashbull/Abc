# features/discover_top10.py
"""Discover Tier Top Movers

For each Discover tier (e.g., 100 ↓, 100↑, 200 ↑, etc.), identify the top N movers
by recent return (1-day, 7-day, 30-day) or by SmartScore.
Pure function only; returns a dict of DataFrames keyed by tier.
"""
from __future__ import annotations

import pandas as pd
from config import DISCOVER_TIERS

__all__ = ["discover_top10"]

def discover_top10(df: pd.DataFrame, n: int = 5) -> dict[str, pd.DataFrame]:
    """Return top N movers per Discover tier.

    Returns:
        { tier_name: DataFrame of top N rows }
    """
    results: dict[str, pd.DataFrame] = {}
    for tier in DISCOVER_TIERS:
        if "discover" not in df.columns:
            results[tier] = pd.DataFrame()
            continue
        tier_df = df[df["discover"] == tier]
        if tier_df.empty:
            results[tier] = pd.DataFrame()
            continue
        # rank by smartscore, then by 7-day returns
        ranked = tier_df.sort_values(
            by=["smartscore", "7_days_returns"],
            ascending=[False, False]
        ).head(n)
        results[tier] = ranked.reset_index(drop=True)
    return results
