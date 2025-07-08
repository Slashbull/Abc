# features/dma_crossover.py
"""DMA Crossover Feature

Detects simple moving average crossovers:
- `dma20_above_50`: True if 20-day > 50-day
- `dma50_above_200`: True if 50-day > 200-day
Pure function only; adds boolean columns.
"""
import pandas as pd

__all__ = ['add_dma_crossover']

def add_dma_crossover(df: pd.DataFrame) -> pd.DataFrame:
    """Return df with DMA crossover boolean columns."""
    work = df.copy()
    # Define SMA column names
    sma20 = '20_day_avg'
    sma50 = '50_day_avg'
    sma200 = '200_day_avg'

    # Check if columns exist
    if all(col in work.columns for col in [sma20, sma50, sma200]):
        work['dma20_above_50'] = work[sma20] > work[sma50]
        work['dma50_above_200'] = work[sma50] > work[sma200]
    else:
        work['dma20_above_50'] = False
        work['dma50_above_200'] = False

    return work
