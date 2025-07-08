# dashboard/app.py
"""M.A.N.T.R.A. · Streamlit front‑end

Single entry‑point.  Binds data pipeline → signal engines → UI.
The UI is intentionally minimal in code lines yet rich in interaction.
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
from signals.volume import add_volume  # to be created
from signals.timing import add_timing  # to be created
from signals.confirmation import add_confirmation  # to be created
from signals.smartscore import add_smartscore  # to be created
from tagging.tagger import apply_tags  # to be created
from alerts.alerts import generate_alerts  # to be created
from features.buy_zone_map import add_buy_zone  # optional feature files
from features.dma_crossover import add_dma_crossover
from features.sector_leaderboard import sector_leaderboard_table  # to be created

# ──────────────────────────────────────────────────────────────────────────────
# 💎  Streamlit page configuration
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title=APP_TITLE, layout="wide")

# Optional: apply light theme colours (works if ~/.streamlit/config.toml absent)
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

# ──────────────────────────────────────────────────────────────────────────────
# 📊 Data Pipeline (cached 30 min via @st.cache_data in ingest layer)
# ──────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=1800)
def load_pipeline() -> pd.DataFrame:
    watch_raw, industry_raw = get_raw_frames()
    df = clean_watchlist(watch_raw)

    # sequentially add signals
    df = add_momentum(df)
    df = add_value(df)
    df = add_volume(df)          # assuming module ready
    df = add_timing(df)
    df = add_confirmation(df)
    df = add_buy_zone(df)        # optional feature for price map
    df = add_dma_crossover(df)   # extra feature
    df = add_smartscore(df)
    df = apply_tags(df, BUY_THRESHOLD, WATCH_THRESHOLD)
    return df


stocks_df = load_pipeline()

# ──────────────────────────────────────────────────────────────────────────────
# 🔍 Sidebar Filters
# ──────────────────────────────────────────────────────────────────────────────
st.sidebar.header("Filters")
sector_sel = st.sidebar.multiselect("Sector", stocks_df["sector"].unique())
cat_sel = st.sidebar.multiselect("Category", stocks_df["category"].unique())
tag_sel = st.sidebar.multiselect("Tag", stocks_df["tag"].unique())
score_min, score_max = st.sidebar.slider("SmartScore Range", 0, 100, (0, 100))

filtered_df = stocks_df.copy()
if sector_sel:
    filtered_df = filtered_df[filtered_df["sector"].isin(sector_sel)]
if cat_sel:
    filtered_df = filtered_df[filtered_df["category"].isin(cat_sel)]
if tag_sel:
    filtered_df = filtered_df[filtered_df["tag"].isin(tag_sel)]
filtered_df = filtered_df.query("@score_min <= smartscore <= @score_max")

# ──────────────────────────────────────────────────────────────────────────────
# 🔔 Alerts Panel
# ──────────────────────────────────────────────────────────────────────────────
alerts = generate_alerts(stocks_df)
if alerts:
    with st.expander("🔔 Alerts", expanded=True):
        for msg in alerts:
            st.warning(msg)

# ──────────────────────────────────────────────────────────────────────────────
# 📈 Sector Dashboard (heatmap / leaderboard)
# ──────────────────────────────────────────────────────────────────────────────
with st.expander("🌐 Sector Leaderboard"):
    st.dataframe(sector_leaderboard_table(stocks_df), use_container_width=True)

# ──────────────────────────────────────────────────────────────────────────────
# 📋 Main Stock Table
# ──────────────────────────────────────────────────────────────────────────────
st.subheader("Stock Screener")
st.dataframe(
    filtered_df.sort_values("smartscore", ascending=False)[
        [
            "ticker",
            "name",
            "current_price",
            "pe",
            "eps_current",
            "smartscore",
            "tag",
            "momentum_score",
            "value_score",
            "volume_score",
            "buy_zone",
            "dma20",
            "dma50",
            "dma200",
        ]
    ],
    use_container_width=True,
)

# ──────────────────────────────────────────────────────────────────────────────
# 🏆 Weekly Top‑10 Auto Watchlist (button)
# ──────────────────────────────────────────────────────────────────────────────
if st.button("🚀 Build Watchlist from Top‑10 SmartScore"):
    top10 = (
        stocks_df.query("smartscore >= @BUY_THRESHOLD and tag == 'BUY'")
        .sort_values("smartscore", ascending=False)
        .head(10)
    )
    st.success(f"Added {len(top10)} stocks to auto‑watchlist snapshot.")
    top10.to_csv("snapshots/weekly_top10.csv", index=False)
    st.dataframe(top10[["ticker", "name", "smartscore", "tag"]])
