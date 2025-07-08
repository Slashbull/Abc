# signals/volume.py
"""Volume Signal

Calculates a **Volume sub-score (0–100)** based on Relative Volume (RVOL)
and recent volume spike detection.  Pure functions only.
"""
from __future__ import annotations

import pandas as pd

__all__ = ["add_volume"]

# Weights for volume components\_WEIGHTS: dict[str, float] = {
    "rvol": 0.6,   # relative volume today vs 90-day average
    "vol_spike": 0.4,  # recent 7-day vs 30-day average spike
}

# Columns mapping
_COLUMN_RVOL: str = "rvol"
_COLUMN_7D_VOL: str = "7_days_volume"
_COLUMN_30D_VOL: str = "30_days_volume"


def add_volume(df: pd.DataFrame) -> pd.DataFrame:
    """Return df with new `volume_score` column (0–100)."""
    work = df.copy()

    # 1️⃣ RVOL percentile (higher is more active)
    if _COLUMN_RVOL in work.columns:
        rvol_scores = work[_COLUMN_RVOL].rank(pct=True).fillna(0)
    else:
        rvol_scores = pd.Series(0.5, index=work.index)

    # 2️⃣ Volume spike: compare 7d vs 30d average
    if _COLUMN_7D_VOL in work.columns and _COLUMN_30D_VOL in work.columns:
        spike = work[_COLUMN_7D_VOL].fillna(0) / work[_COLUMN_30D_VOL].replace(0, pd.NA)
        spike_scores = spike.rank(pct=True).fillna(0)
    else:
        spike_scores = pd.Series(0.5, index=work.index)

    # Composite raw score
    raw = (
        _WEIGHTS["rvol"] * rvol_scores
        + _WEIGHTS["vol_spike"] * spike_scores
    )

    work["volume_score"] = (raw.rank(pct=True) * 100).round(2)
    return work
