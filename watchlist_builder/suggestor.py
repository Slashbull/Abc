# watchlist_builder/suggestor.py
"""Watchlist Builder

Automatically constructs a prioritized watchlist from the DataFrame based on
SmartScore, tags, and optional filters. Returns the watchlist as a DataFrame.
Pure function only.
"""
from __future__ import annotations

import pandas as pd
from typing import Optional

__all__ = ['build_watchlist']

def build_watchlist(
    df: pd.DataFrame,
    tag: Optional[str] = None,
    min_score: Optional[float] = None,
    max_items: int = 50
) -> pd.DataFrame:
    """
    Build a watchlist by filtering on tag and SmartScore threshold,
    then returning the top `max_items` stocks sorted by SmartScore.

    Args:
        df: DataFrame with `smartscore` and `tag` columns.
        tag: If set, filter by this tag (e.g., '🟢 BUY').
        min_score: If set, only include stocks with SmartScore >= min_score.
        max_items: Maximum number of items in the watchlist.

    Returns:
        A DataFrame of the selected watchlist.
    """
    work = df.copy()

    if tag:
        work = work[work['tag'] == tag]
    if min_score is not None:
        work = work[work['smartscore'] >= min_score]

    watch = (
        work.sort_values('smartscore', ascending=False)
        .head(max_items)
        .reset_index(drop=True)
    )
    return watch
