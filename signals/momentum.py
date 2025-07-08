# signals/momentum.py
"""Momentum Signal

Calculates a **Momentum sub‑score (0–100)** based on weighted returns
from multiple time‑frames.  The function is *pure* (stateless) and never
performs I/O.
"""
from __future__ import annotations

import pandas as pd

__all__ = ["add_momentum"]

# ---------------------------------------------------------------------------
# 🏋️‍♀️ Weights – tweak freely or expose via config later
# ---------------------------------------------------------------------------

_WEIGHTS: dict[str, float] = {
    "one_day": 0.10,     # column 1_day_change (% already cleaned, numeric)
    "seven_day": 0.15,   # 7_days_returns
    "thirty_day": 0.20,  # 30_days_returns
    "three_month": 0.20, # 3_months
    "six_month": 0.20,   # 6_months
    "one_year": 0.15,    # 1_year
}

_COLUMNS_MAP: dict[str, str] = {
    "one_day": "1_day_change",
    "seven_day": "7_days_returns",
    "thirty_day": "30_days_returns",
    "three_month": "3_months",
    "six_month": "6_months",
    "one_year": "1_year",
}


# ---------------------------------------------------------------------------
# 🧮 Public function
# ---------------------------------------------------------------------------

def add_momentum(df: pd.DataFrame) -> pd.DataFrame:  # noqa: WPS231 length ok
    """Return *df* with a new `momentum_score` column (0‑100).

    Steps
    -----
    1. Weighted sum of percentage returns (missing values treated as 0).
    2. Rank‑percentile across universe → 0‑100 score.
    """
    work = df.copy()

    # 1️⃣ Weighted raw momentum value (not yet scaled 0‑100)
    momentum_raw = pd.Series(0.0, index=work.index)
    for key, weight in _WEIGHTS.items():
        col = _COLUMNS_MAP[key]
        if col in work.columns:
            momentum_raw += work[col].fillna(0) * weight

    # 2️⃣ Convert to percentile 0‑100 (higher = stronger momentum)
    momentum_score = momentum_raw.rank(pct=True) * 100.0

    work["momentum_score"] = momentum_score.round(2)
    return work
