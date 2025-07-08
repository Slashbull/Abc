# signals/smartscore.py
"""SmartScore Signal

Aggregates all sub-scores into a composite SmartScore (0–100) using
the weights defined in config.SMART_WEIGHTS.
Pure function only.
"""
from __future__ import annotations

import pandas as pd
from config import SMART_WEIGHTS

__all__ = ["add_smartscore"]

# Mapping of config keys to DataFrame column names
_SCORE_COLS: dict[str, str] = {
    "momentum": "momentum_score",
    "value": "value_score",
    "volume": "volume_score",
    "timing": "timing_score",
    "confirmation": "confirmation_score",
    "buy_zone": "buy_zone_score",  # ensure feature adds this or default
}


def add_smartscore(df: pd.DataFrame) -> pd.DataFrame:
    """Return df with new `smartscore` column (0–100)."""
    work = df.copy()
    total_weight = sum(SMART_WEIGHTS.values())

    # accumulate weighted normalized scores
    raw = pd.Series(0.0, index=work.index)
    for key, weight in SMART_WEIGHTS.items():
        col = _SCORE_COLS.get(key)
        if col and col in work.columns:
            # sub-score is 0–100; convert to 0–1, weight, then accumulate
            raw += (work[col].fillna(0) / 100.0) * weight

    # Normalize to 0–100
    work["smartscore"] = ((raw / total_weight) * 100).round(2)
    return work
