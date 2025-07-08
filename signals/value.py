# signals/value.py
"""Value Signal

Generates a **Value sub‑score (0–100)** combining:
1. Low PE relative to universe (lower = better)
2. High EPS growth (EPS % Change)
3. Discount from 52‑week high (Pct_From_High → deeper discount = better)
4. Price below DMA200 (greater negative gap = better)

All maths are percentile‑based so the score is automatically scaled across any
universe size.
"""
from __future__ import annotations

import pandas as pd

__all__ = ["add_value"]

# ──────────────────────────────────────────────────────────────────────────────
# ⚖️ Weights (edit in one place)
# ──────────────────────────────────────────────────────────────────────────────

_WEIGHTS: dict[str, float] = {
    "pe": 0.25,
    "eps_change": 0.30,
    "discount_52w": 0.25,
    "below_dma200": 0.20,
}


# ──────────────────────────────────────────────────────────────────────────────
# 🧮 Helpers
# ──────────────────────────────────────────────────────────────────────────────

def _percentile(series: pd.Series, higher_is_better: bool = True) -> pd.Series:  # noqa: WPS110
    """Return series ranked 0…1 (percentile)."""
    ranked = series.rank(pct=True)
    return ranked if higher_is_better else 1 - ranked


def _safe_ratio(num: pd.Series, den: pd.Series) -> pd.Series:  # noqa: WPS110
    with pd.option_context("mode.use_inf_as_na", True):  # ignore divide‑by‑zero
        ratio = num / den
    return ratio.replace([pd.NA, pd.NaT], 0).fillna(0)


# ──────────────────────────────────────────────────────────────────────────────
# 🏦 Value‑score generator
# ──────────────────────────────────────────────────────────────────────────────

def add_value(df: pd.DataFrame) -> pd.DataFrame:  # noqa: WPS231 length ok
    work = df.copy()

    # 1️⃣ PE (lower better)
    if "pe" in work.columns:
        work["_pe_score"] = _percentile(work["pe"], higher_is_better=False)
    else:
        work["_pe_score"] = 0.5  # neutral if missing

    # 2️⃣ EPS growth (higher better)
    eps_col = "eps_pct_change" if "eps_pct_change" in work.columns else "eps_change"
    if eps_col in work.columns:
        work["_eps_score"] = _percentile(work[eps_col].fillna(0), higher_is_better=True)
    else:
        work["_eps_score"] = 0.5

    # 3️⃣ Discount from 52‑week high (more negative = better value)
    if "pct_from_high" in work.columns:
        # pct_from_high already negative numbers for discount; invert sign
        work["_52w_score"] = _percentile(-work["pct_from_high"].fillna(0), True)
    else:
        work["_52w_score"] = 0.5

    # 4️⃣ Price below DMA200 (% gap)
    if {"current_price", "200_day_avg"}.issubset(work.columns):
        below = 1 - _safe_ratio(work["current_price"], work["200_day_avg"].replace(0, pd.NA))
        work["_dma200_score"] = _percentile(below.fillna(0), True)
    else:
        work["_dma200_score"] = 0.5

    # 5️⃣ Composite Value Score (0‑100)
    value_raw = (
        _WEIGHTS["pe"] * work["_pe_score"]
        + _WEIGHTS["eps_change"] * work["_eps_score"]
        + _WEIGHTS["discount_52w"] * work["_52w_score"]
        + _WEIGHTS["below_dma200"] * work["_dma200_score"]
    )
    work["value_score"] = (value_raw * 100).round(2)

    # Drop helper cols
    work.drop(columns=[c for c in work.columns if c.startswith("_")], inplace=True)
    return work
