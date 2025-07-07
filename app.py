# app.py

import streamlit as st
import pandas as pd
from data_loader import load_watchlist_data
from scoring_logic import calculate_score

# Streamlit settings
st.set_page_config(page_title="Stock Intelligence | M.A.N.T.R.A.", layout="wide")

# Header
st.title("📊 M.A.N.T.R.A. Stock Intelligence Dashboard")
st.markdown("A ruthless, smart, and emotionless way to discover top investment opportunities.")

# Load and score data
df = load_watchlist_data()
if df.empty:
    st.error("❌ No data loaded from Google Sheet.")
    st.stop()

df = calculate_score(df)

# Sidebar filters
st.sidebar.header("🔎 Filter Stocks")
sector = st.sidebar.multiselect("Sector", sorted(df['Sector'].dropna().unique()), default=None)
category = st.sidebar.multiselect("Market Cap Category", sorted(df['Category'].dropna().unique()), default=None)
min_score = st.sidebar.slider("Min MANTRA Score", 0, 100, 60)
price_range = st.sidebar.slider("Price Range", 0, int(df['Current_Price'].max()), (0, int(df['Current_Price'].max())))

# Apply filters
filtered_df = df.copy()

if sector:
    filtered_df = filtered_df[filtered_df['Sector'].isin(sector)]
if category:
    filtered_df = filtered_df[filtered_df['Category'].isin(category)]

filtered_df = filtered_df[
    (filtered_df['MANTRA_Score'] >= min_score) &
    (filtered_df['Current_Price'] >= price_range[0]) &
    (filtered_df['Current_Price'] <= price_range[1])
]

# Main table
st.subheader("📈 Top Ranked Stocks by MANTRA Score")
st.dataframe(
    filtered_df[['Ticker', 'Name', 'Sector', 'Current_Price', 'Enter_Price_Target', 'PE', 'EPS_Change', '1_Year', 'RVOL', 'MANTRA_Score']].sort_values(by='MANTRA_Score', ascending=False).reset_index(drop=True),
    use_container_width=True
)

# Optional: Detailed company view
selected_ticker = st.selectbox("🔍 View Details for Ticker", options=filtered_df['Ticker'].unique())
if selected_ticker:
    stock = filtered_df[filtered_df['Ticker'] == selected_ticker].squeeze()
    st.markdown(f"### 🧾 Details: {stock['Name']}")
    st.write({
        "Market Cap": stock.get("Market_Cap", ""),
        "Sector": stock.get("Sector", ""),
        "Industry": stock.get("Industry", ""),
        "Current Price": stock.get("Current_Price", ""),
        "Target Price": stock.get("Enter_Price_Target", ""),
        "PE": stock.get("PE", ""),
        "EPS Growth %": stock.get("EPS_Change", ""),
        "1-Year Return": stock.get("1_Year", ""),
        "RVOL": stock.get("RVOL", ""),
        "Score": stock.get("MANTRA_Score", "")
    })
