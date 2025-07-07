# scoring_logic.py

import pandas as pd
import numpy as np

def calculate_score(df: pd.DataFrame) -> pd.DataFrame:
    # Safety: Avoid errors if column missing
    def safe_col(col):
        return df[col] if col in df.columns else np.nan

    # Scoring factors with weights
    weights = {
        'EPS_Change': 20,  # EPS YoY change
        'PE': 15,  # Low PE = better
        'Price_vs_200DMA': 10,  # Price < 200DMA = reversion opp
        'Near_Buy_Target': 10,  # If price is near your target
        'RVOL': 15,  # Volume surge
        '1_Year': 20,  # Strong recent trend
        'Sector_Momentum_Bonus': 10  # Optional (future)
    }

    # Create derived columns
    df['Price_vs_200DMA'] = safe_col('Current_Price') - safe_col('200_Day_Avg')
    df['Near_Buy_Target'] = np.where(
        safe_col('Pct_Drop_needed_for_Buy_Target') <= 5, 1, 0
    )

    # Normalize features (0-1 scale)
    def normalize(series):
        return (series - series.min()) / (series.max() - series.min())

    score = (
        normalize(safe_col('EPS_Change')) * weights['EPS_Change'] +
        (1 - normalize(safe_col('PE'))) * weights['PE'] +
        (1 - normalize(df['Price_vs_200DMA'])) * weights['Price_vs_200DMA'] +
        df['Near_Buy_Target'] * weights['Near_Buy_Target'] +
        normalize(safe_col('RVOL')) * weights['RVOL'] +
        normalize(safe_col('1_Year')) * weights['1_Year']
        # + sector momentum logic later
    )

    df['MANTRA_Score'] = score.round(2)
    return df.sort_values(by='MANTRA_Score', ascending=False)
