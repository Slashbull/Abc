# app.py

import streamlit as st
from data_loader import load_watchlist_data

st.set_page_config(page_title="📊 Stock Dashboard", layout="wide")

# Load the stock watchlist data
df = load_watchlist_data()

# DEBUG: Print all columns for verification
st.sidebar.write("📋 Columns:", df.columns.tolist())

# Show first 50 stocks preview
st.subheader("🧾 First 50 Stocks Preview")
if df.empty:
    st.warning("No data available. Please check the source sheet or load configuration.")
else:
    st.dataframe(df.head(50))

# Filters
st.sidebar.header("🔎 Filter Stocks")

# Sector filter (guarded)
sector_list = df["Sector"].dropna().unique().tolist() if "Sector" in df.columns else []
selected_sector = st.sidebar.selectbox("Select Sector", ["All"] + sorted(sector_list)) if sector_list else None

# Market Cap filter (optional)
market_caps = df["Category"].dropna().unique().tolist() if "Category" in df.columns else []
selected_cap = st.sidebar.selectbox("Select Market Cap", ["All"] + sorted(market_caps)) if market_caps else None

# Apply filters
filtered_df = df.copy()

if selected_sector and selected_sector != "All":
    filtered_df = filtered_df[filtered_df["Sector"] == selected_sector]

if selected_cap and selected_cap != "All":
    filtered_df = filtered_df[filtered_df["Category"] == selected_cap]

# Display filtered data
st.subheader("📈 Filtered Watchlist")
st.write(f"Showing {len(filtered_df)} out of {len(df)} stocks")
st.dataframe(filtered_df.reset_index(drop=True))
