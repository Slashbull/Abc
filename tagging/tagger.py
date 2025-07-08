# tagging/tagger.py
"""Tagging Module

Assigns a `tag` to each stock based on its SmartScore and thresholds in config.
Possible tags:
  - '🟢 BUY'
  - '🟡 WATCH'
  - '🔴 AVOID'
"""
from __future__ import annotations

import pandas as pd
from config import BUY_THRESHOLD, WATCH_THRESHOLD

__all__ = ["apply_tags"]


def apply_tags(df: pd.DataFrame, buy_th: int = BUY_THRESHOLD, watch_th: int = WATCH_THRESHOLD) -> pd.DataFrame:
    """Return df with new `tag` column based on SmartScore thresholds."""
    work = df.copy()
    def tag_row(score: float) -> str:
        if score >= buy_th:
            return '🟢 BUY'
        if score >= watch_th:
            return '🟡 WATCH'
        return '🔴 AVOID'

    work['tag'] = work['smartscore'].fillna(0).apply(tag_row)
    return work
