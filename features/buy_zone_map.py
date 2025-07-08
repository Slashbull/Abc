# features/buy_zone_map.py
"""Buy Zone Map Feature

Calculates a `buy_zone_score` (0–100) based on proximity of current price to key
technical levels: 20 DMA, 50 DMA, 200 DMA, and 52-week low/high.
Pure function only; adds `buy_zone_score` column.
"""
from __future__ import annotations

import pandas as pd

def add_buy_zone(df: pd.DataFrame) -> pd.DataFrame:
    """Return df with new `buy_zone_score` column (0–100)."""
    work = df.copy()

    # Ensure required columns exist
    cols = {
        'price': 'current_price',
        'dma20': '20_day_avg',
        'dma50': '50_day_avg',
        'dma200': '200_day_avg',
        'low52': '52_week_low',
        'high52': '52_week_high'
    }
    # Compute proximity metrics (0–1): closer to support = higher
    metrics = []
    if all(c in work.columns for c in cols.values()):
        price = work[cols['price']]
        # Distance to DMAs: 1 - (price - dma)/price
        prox20 = 1 - (price - work[cols['dma20']]) / price
        prox50 = 1 - (price - work[cols['dma50']]) / price
        prox200 = 1 - (price - work[cols['dma200']]) / price
        # Discount from high: (high52 - price)/high52
        disc_high = (work[cols['high52']] - price) / work[cols['high52']]
        # Proximity to low: 1 - (price - low52)/price
        prox_low = 1 - (price - work[cols['low52']]) / price
        metrics = [prox20, prox50, prox200, disc_high, prox_low]
    else:
        # if missing, default neutral metrics
        metrics = [pd.Series(0.5, index=work.index)] * 5

    # Combine metrics as average then percentile scale
    raw = sum(m.fillna(0) for m in metrics) / len(metrics)
    # percentile rank to 0–100
    work['buy_zone_score'] = raw.rank(pct=True).mul(100).round(2)
    return work

__all__ = ['add_buy_zone']
