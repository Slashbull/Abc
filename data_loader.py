import pandas as pd
import numpy as np
from config import GOOGLE_SHEET_CSV_URL

def load_watchlist_data():
    try:
        # Load the CSV and skip first 3 metadata rows
        df = pd.read_csv(GOOGLE_SHEET_CSV_URL, skiprows=3)

        # Drop unnamed or empty columns
        df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

        # Clean column names
        df.columns = (
            df.columns
            .str.strip()
            .str.replace('↓', '', regex=False)
            .str.replace('%', 'Pct', regex=False)
            .str.replace('(', '', regex=False)
            .str.replace(')', '', regex=False)
            .str.replace('/', '_', regex=False)
            .str.replace(' ', '_', regex=False)
            .str.replace('__', '_', regex=False)
        )

        # Rename Ticker Column
        df.rename(columns={'Enter_Ticker': 'Ticker'}, inplace=True)

        # Drop rows with no ticker
        df.dropna(subset=['Ticker'], inplace=True)

        # List of numeric columns (clean ₹, commas, %, arrows)
        to_numeric_cols = [
            'Current_Price', '52_Week_LOW', '52_Week_HIGH', 'Pct_From_Low', 'Pct_From_High',
            '20_Day_Avg', '50_Day_Avg', '200_Day_Avg', '3_Days_Returns', '7_Days_Returns',
            '30_Days_Returns', '3_Months', '6_Months', '1_Year', '3_Year', '5_Year',
            'Volume', '7_Days_Volume', '30_Days_Volume', '3_Months_Volume',
            '1_day_vs._90_day', '7_day_vs._90_day', '30_day_vs._90_day',
            'RVOL', 'Prev_Close', 'PE', 'EPS_Current', 'EPS_Last_Qtr', 'EPS_TTM', 'EPS_Change'
        ]

        for col in to_numeric_cols:
            if col in df.columns:
                df[col] = (
                    df[col]
                    .astype(str)
                    .str.replace('₹', '', regex=False)
                    .str.replace(',', '', regex=False)
                    .str.replace('%', '', regex=False)
                    .str.replace('▲', '', regex=False)
                    .str.replace('▼', '-', regex=False)
                    .str.strip()
                )
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Strip any arrows or unicode in 'Discover' column
        if 'Discover' in df.columns:
            df['Discover'] = df['Discover'].astype(str).str.replace('↑', '').str.replace('↓', '').str.strip()

        return df

    except Exception as e:
        print("❌ Error loading watchlist:", e)
        return pd.DataFrame()
