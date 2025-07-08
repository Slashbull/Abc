# features/eps_growth_screener.py
"""EPS Growth Screener Feature

Identifies stocks with strong EPS growth relative to the universe.
Calculates a `eps_growth_score` (0–100) based on percentile rank of
`eps_pct_change` (or fallback to `eps_change`).
Pure function only; adds `eps_growth_score` column.
"""
from __future__ import annotations

import pandas as pd

__all__ = ['add_eps_growth_score']

def add_eps_growth_score(df: pd.DataFrame) -> pd.DataFrame:
    """Return df with new `eps_growth_score` column (0–100)."""
    work = df.copy()
    # Determine EPS change column
    if 'eps_pct_change' in work.columns:
        eps_col = 'eps_pct_change'
    elif 'eps_change' in work.columns:
        eps_col = 'eps_change'
    else:
        # No EPS change data; assign neutral
        work['eps_growth_score'] = 50.0
        return work

    # Percentile rank of EPS growth (higher is better)
    eps_vals = work[eps_col].fillna(0)
    eps_pct = eps_vals.rank(pct=True)
    work['eps_growth_score'] = (eps_pct * 100).round(2)
    return work
