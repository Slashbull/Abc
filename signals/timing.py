# signals/timing.py
"""Timing Signal

Detects key DMA crossovers and buy-zone proximity as timing signals.
Calculates a **Timing sub-score (0–100)** based on:
1. Number of bullish DMA crossovers (20>50, 50>200)
2. Proximity to DMA20 and DMA50 (closer above = better)
3. Proximity to 52-week low (closer to low = better for dip buys)

Pure functions only; no I/O.
"""
from __future__ import annotations

import pandas as pd

__all__ = ["add_timing"]

# Weights for timing components\_WEIGHTS: dict[str, float] = {
    "dma_cross": 0.5,   # crossover count
    "prox_dma": 0.3,    # distance above DMA20/50
    "prox_low": 0.2,    # proximity to 52-week low
}

# Columns
_COL_PRICE: str = "current_price"
_COL_DMA20: str = "20_day_avg"
_COL_DMA50: str = "50_day_avg"
_COL_DMA200: str = "200_day_avg"
_COL_LOW52: str = "52_week_low"


def add_timing(df: pd.DataFrame) -> pd.DataFrame:
    """Return df with new `timing_score` column (0–100)."""
    work = df.copy()

    # 1️⃣ DMA crossover score: count of bull signals
    cross = pd.Series(0, index=work.index)
    has = lambda a, b: (work[a] > work[b]).astype(int)
    cross += has(_COL_DMA20, _COL_DMA50)
    cross += has(_COL_DMA50, _COL_DMA200)
    cross_pct = cross / 2.0  # 0, .5, or 1

    # 2️⃣ Proximity to DMA20 & DMA50: price - DMA / price
    prox_dma20 = (work[_COL_PRICE] - work[_COL_DMA20]) / work[_COL_PRICE]
    prox_dma50 = (work[_COL_PRICE] - work[_COL_DMA50]) / work[_COL_PRICE]
    prox_dma = ((prox_dma20 + prox_dma50) / 2).fillna(0)
    prox_dma_pct = prox_dma.rank(pct=True)

    # 3️⃣ Proximity to 52W low: 1 - (price - low)/price  (closer to low=>higher)
    prox_low = 1 - ((work[_COL_PRICE] - work[_COL_LOW52]) / work[_COL_PRICE])
    prox_low_pct = prox_low.rank(pct=True)

    # Composite raw
    raw = (
        _WEIGHTS["dma_cross"] * cross_pct
        + _WEIGHTS["prox_dma"] * prox_dma_pct
        + _WEIGHTS["prox_low"] * prox_low_pct
    )

    work["timing_score"] = (raw.rank(pct=True) * 100).round(2)
    return work
