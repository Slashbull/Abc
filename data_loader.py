import pandas as pd
import numpy as np
from config import GOOGLE_SHEET_CSV_URL

def load_watchlist_data():
    try:
        # Step 1: Load raw data from Google Sheet with proper encoding
        df = pd.read_csv(GOOGLE_SHEET_CSV_URL, encoding='utf-8', on_bad_lines='skip')

        # Step 2: Display original columns for debug
        print("🧾 Raw columns:", df.columns.tolist())

        # Step 3: Clean column names
        df.columns = (
            df.columns
            .str.strip()
            .str.replace(' ', '_', regex=False)
            .str.replace('↓', '', regex=False)
            .str.replace('%', 'Pct', regex=False)
            .str.replace('(', '', regex=False)
            .str.replace(')', '', regex=False)
            .str.replace('/', '_', regex=False)
            .str.replace('__', '_', regex=False)
        )

        # Step 4: Attempt to find the Ticker column
        ticker_col = None
        for col in df.columns:
            if "Ticker" in col:
                ticker_col = col
                break

        if ticker_col:
            df.rename(columns={ticker_col: 'Ticker'}, inplace=True)
            df.dropna(subset=['Ticker'], inplace=True)
        else:
            print("⚠️ No column containing 'Ticker' found")
            df['Ticker'] = np.nan

        # Step 5: Clean weird characters from data
        def clean_text(x):
            if isinstance(x, str):
                return (
                    x.replace('â‚¹', '')
                     .replace('â–²', '')
                     .replace('â–¼', '')
                     .replace('â†‘', '')
                     .replace('â†“', '')
                     .replace(',', '')
                     .strip()
                )
            return x

        df = df.applymap(clean_text)

        # Step 6: Convert selected columns to numeric (if they exist)
        numeric_columns = [
            'Enter_Price_Target', 'Pct_Drop_needed_for_Buy_Target', 'Current_Price',
            '52_Week_LOW', '52_Week_HIGH', 'Pct_From_Low', 'Pct_From_High',
            '20_Day_Avg', '50_Day_Avg', '200_Day_Avg', '3_Days_Returns',
            '7_Days_Returns', '30_Days_Returns', '3_Months', '6_Months',
            '1_Year', '3_Year', '5_Year', 'Volume', '7_Days_Volume',
            '30_Days_Volume', '3_Months_Volume', '1_day_vs._90_day',
            '7_day_vs._90_day', '30_day_vs._90_day', 'RVOL', 'Prev_Close',
            'PE', 'EPS_Current', 'EPS_Last_Qtr', 'EPS_TTM', 'EPS_Change'
        ]

        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        return df

    except Exception as e:
        print("❌ Error loading Watchlist data:", e)
        return pd.DataFrame()
