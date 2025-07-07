# mantra_engine.py

import pandas as pd
from data_loader import load_watchlist_data
from scoring_logic import score_stock

def run_mantra_engine():
    df = load_watchlist_data()
    if df.empty:
        return pd.DataFrame()

    # Apply scoring logic to each stock row
    df['Signal'] = df.apply(score_stock, axis=1)

    # Tag for filtering
    df['Tag'] = df['Signal'].apply(lambda x: '🟢 BUY' if x == 'BUY' else '🟡 WATCH' if x == 'WATCH' else '🔴 AVOID')

    return df

if __name__ == "__main__":
    result_df = run_mantra_engine()
    print(result_df[['Ticker', 'Current_Price', 'Signal', 'Tag']].head())
