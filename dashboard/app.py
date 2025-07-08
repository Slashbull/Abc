# dashboard/app.py
"""M.A.N.T.R.A. · Streamlit front-end

Single entry-point.  Binds data pipeline → signal engines → UI.
"""
from __future__ import annotations

import pandas as pd
import streamlit as st

from config import (
    APP_TITLE,
    LIGHT_THEME,
    BUY_THRESHOLD,
    WATCH_THRESHOLD,
)
from ingest.ingest import get_raw_frames
from clean.clean import clean_watchlist, clean_industry
from signals.momentum import add_momentum
from signals.value import add_value
from signals.volume import add_volume
from signals.timing import add_timing
from signals.confirmation import add_confirmation
from signals.smartscore import add_smartscore
from tagging.tagger import apply_tags
from alerts.alerts import generate_alerts
from alerts.alert_ui import show_alerts
from features.buy_zone_map import add_buy_zone
from features.dma_crossover import add_dma_crossover
from features.eps_growth_screener import add_eps_growth_score
from features.sector_leaderboard import sector_leaderboard_table
from features.discover_top10 import discover_top10
from watchlist_builder.suggestor import build_watchlist

# ─────────────────────────────────────────────────────────
# Page config & theming
# ─────────────────────────────────────────────────────────
st.set_page_config(page_title=APP_TITLE, layout="wide")
st.markdown(
    f"""
    <style>
        :root {{
            --primary-color: {LIGHT_THEME['primaryColor']};
            --background-color: {LIGHT_THEME['backgroundColor']};
            --secondary-background-color: {LIGHT_THEME['secondaryBackgroundColor']};
            --text-color: {LIGHT_THEME['textColor']};
        }}
    </style>
    """,
    unsafe_allow_html=True,
)
st.title(APP_TITLE)

# ─────────────────────────────────────────────────────────
# Data pipeline (cached)
# ─────────────────────────────────────────────────────────
@st.cache_data(ttl=1800)
def load_pipeline() -> pd.DataFrame:
    watch_raw, industry_raw = get_raw_frames()
    df = clean_watchlist(watch_raw)

    # Signals
    df = add_momentum(df)
    df = add_value(df)
    df = add_volume(df)
    df = add_timing(df)
    df = add_confirmation(df)
    df = add_buy_zone(df)
    df = add_dma_crossover(df)
    df = add_eps_growth_score(df)
    df = add_smartscore(df)
    df = apply_tags(df, BUY_THRESHOLD, WATCH_THRESHOLD)
    return df

stocks_df = load_pipeline()

# ─────────────────────────────────────────────────────────
# Sidebar filters
# ─────────────────────────────────────────────────────────
st.sidebar.header("Filters")
sector_sel = st.sidebar.multiselect("Sector", stocks_df["sector"].unique())
category_sel = st.sidebar.multiselect("Category", stocks_df["category"].unique())
tag_sel = st.sidebar.multiselect("Tag", stocks_df["tag"].unique())
score_min, score_max = st.sidebar.slider("SmartScore Range", 0, 100, (0, 100))

filtered = stocks_df.copy()
if sector_sel:
    filtered = filtered[filtered["sector"].isin(sector_sel)]
if category_sel:
    filtered = filtered[filtered["category"].isin(category_sel)]
if tag_sel:
    filtered = filtered[filtered["tag"].isin(tag_sel)]
filtered = filtered.query("@score_min <= smartscore <= @score_max")

# ─────────────────────────────────────────────────────────
# Alerts
# ─────────────────────────────────────────────────────────
alerts = generate_alerts(stocks_df)
show_alerts(alerts)

# ─────────────────────────────────────────────────────────
# Sector leaderboard
# ─────────────────────────────────────────────────────────
with st.expander("🌐 Sector Leaderboard", expanded=True):
    st.dataframe(sector_leaderboard_table(stocks_df), use_container_width=True)

# ─────────────────────────────────────────────────────────
# Main stock table
# ─────────────────────────────────────────────────────────
st.subheader("Stock Screener")
display_cols = [
    "ticker", "name", "current_price", "pe", "eps_current",
    "smartscore", "tag", "momentum_score", "value_score",
    "volume_score", "buy_zone_score", "dma20_above_50", "dma50_above_200"
]
st.dataframe(filtered[display_cols].sort_values("smartscore", ascending=False),
             use_container_width=True)

# ─────────────────────────────────────────────────────────
# Discover Top-10 Movers
# ─────────────────────────────────────────────────────────
with st.expander("🏅 Discover Tier Top Movers"):
    tops = discover_top10(stocks_df, n=5)
    for tier, df_tier in tops.items():
        if not df_tier.empty:
            st.markdown(f"**{tier}**")
            st.table(df_tier[["ticker", "smartscore", "7_days_returns"]])

# ─────────────────────────────────────────────────────────
# Auto-watchlist builder
# ─────────────────────────────────────────────────────────
st.sidebar.markdown("---")
if st.sidebar.button("🚀 Build Auto Watchlist (Top 50)"):
    wl = build_watchlist(stocks_df, tag="🟢 BUY", max_items=50)
    st.sidebar.dataframe(wl[["ticker", "smartscore"]])
