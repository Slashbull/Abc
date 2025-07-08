# features/sector_leaderboard.py
"""Sector Leaderboard Feature

Aggregates stock-level metrics into sector-level summaries, including:
- Average SmartScore
- Percentage of stocks outperforming (e.g., >0% 1Y return)
- Sector risk score (volatility-adjusted returns)

Pure function only; takes DataFrame and returns a new DataFrame for display.
"""
import pandas as pd

__all__ = ['sector_leaderboard_table']

def sector_leaderboard_table(df: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame summarizing metrics per sector."""
    work = df.copy()
    # Ensure required columns
    required = ['sector', 'smartscore', '1_year', '3_year', '5_year']
    for col in required:
        if col not in work.columns:
            work[col] = pd.NA
    # Group by sector
    grp = work.groupby('sector')
    # Build summary
    summary = pd.DataFrame({
        'avg_smartscore': grp['smartscore'].mean().round(2),
        'count':          grp.size(),
        'pct_up_1y':      grp.apply(lambda x: (x['1_year'] > 0).mean() * 100).round(2),
        'volatility_1y':  grp['1_year'].std().round(2),
        'avg_return_3y':  grp['3_year'].mean().round(2),
        'avg_return_5y':  grp['5_year'].mean().round(2),
    })
    # Rank sectors by avg_smartscore
    summary['rank'] = summary['avg_smartscore'].rank(ascending=False).astype(int)
    return summary.reset_index().sort_values('rank')
