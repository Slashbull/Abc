# signals/confirmation.py
"""Confirmation Signal

Generates a **Confirmation sub-score (0–100)** by combining momentum
and volume signals to filter out false moves (e.g., price moves without volume).
Pure functions only.
"""
from __future__ import annotations

import pandas as pd

__all__ = ["add_confirmation"]

# Weights for confirmation
_WEIGHTS: dict[str, float] = {
    "momentum": 0.5,
    "volume":   0.5,
}

# Corresponding score columns
_COL_MOM: str = "momentum_score"
_COL_VOL: str = "volume_score"


def add_confirmation(df: pd.DataFrame) -> pd.DataFrame:
    """Return df with new `confirmation_score` column (0–100)."""
    work = df.copy()

    # Extract percent values [0–100] → normalize to [0–1]
    mom = work[_COL_MOM].fillna(0) / 100.0 if _COL_MOM in work.columns else 0
    vol = work[_COL_VOL].fillna(0) / 100.0 if _COL_VOL in work.columns else 0

    raw = (_WEIGHTS["momentum"] * mom) + (_WEIGHTS["volume"] * vol)
    work["confirmation_score"] = (raw.rank(pct=True) * 100).round(2)
    return work
