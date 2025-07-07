import streamlit as st
import pandas as pd

# ---------------------------
# STEP 1: Load Your Sheet
# ---------------------------

st.set_page_config(page_title="📈 Stock Watchlist", layout="wide")

st.title("📊 Stock Watchlist Dashboard")
st.markdown("Built by Wasim using Google Sheets + Streamlit")

# Replace with your own Sheet URL and sheet name
sheet_url = "https://docs.google.com/spreadsheets/d/1XipQ2_Cap60A9tfxDmmaXInsz_xFE42VtwVIQyUL-Hs/gviz/tq?tqx=out:csv&sheet=Watchlist"

try:
    df = pd.read_csv(sheet_url)
    st.success("✅ Google Sheet loaded successfully")
except Exception as e:
    st.error("❌ Failed to load Google Sheet. Please check sharing settings.")
    st.stop()

# ---------------------------
# STEP 2: Display Preview
# ---------------------------

st.subheader("🧾 First 50 Stocks Preview")
st.dataframe(df.head(50), use_container_width=True)

# Optional: Filter by Sector or Category
with st.sidebar:
    st.header("🔍 Filters")
    sectors = df["Sector"].dropna().unique().tolist()
    selected_sector = st.selectbox("Filter by Sector", ["All"] + sectors)

if selected_sector != "All":
    df = df[df["Sector"] == selected_sector]

st.subheader(f"📄 Filtered Stocks ({len(df)})")
st.dataframe(df, use_container_width=True)
