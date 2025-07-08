# alerts/alerts.py
"""Alerts Module

Generates in-app alerts based on the latest DataFrame signals.
Pure logic: reads DataFrame, returns list of message strings.
"""
from __future__ import annotations

import pandas as pd
from config import BUY_THRESHOLD

__all__ = ["generate_alerts"]


def generate_alerts(df: pd.DataFrame) -> list[str]:
    """Return list of alert messages for the UI to display."""
    alerts: list[str] = []

    # 1️⃣ New Buy Opportunities
    buy_df = df[df['tag'] == '🟢 BUY']
    if not buy_df.empty:
        top_buys = buy_df.nlargest(5, 'smartscore')
        tickers = top_buys['ticker'].tolist()
        alerts.append(
            f"🚀 Top Buy Candidates: {', '.join(tickers)}"
        )

    # 2️⃣ Momentum Spike
    if 'momentum_score' in df.columns:
        high_mom = df[df['momentum_score'] >= 90]
        if not high_mom.empty:
            symbols = high_mom['ticker'].tolist()
            alerts.append(
                f"📈 High Momentum Alert: {', '.join(symbols[:5])}" + (
                    '...' if len(symbols) > 5 else ''
                )
            )

    # 3️⃣ Volume Surge
    if 'volume_score' in df.columns:
        high_vol = df[df['volume_score'] >= 90]
        if not high_vol.empty:
            symbols = high_vol['ticker'].tolist()
            alerts.append(
                f"🔔 Volume Spike Alert: {', '.join(symbols[:5])}" + (
                    '...' if len(symbols) > 5 else ''
                )
            )

    # 4️⃣ Mixed Signals: low value but strong momentum
    if {'value_score', 'momentum_score'}.issubset(df.columns):
        mixed = df[(df['value_score'] <= 30) & (df['momentum_score'] >= 70)]
        if not mixed.empty:
            syms = mixed['ticker'].tolist()
            alerts.append(
                f"⚖️ Contrast Alert (Value & Momentum): {', '.join(syms[:5])}" + (
                    '...' if len(syms) > 5 else ''
                )
            )

    return alerts
