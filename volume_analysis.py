# volume_analysis.py

def is_volume_breakout(row, threshold=50):
    """
    Detects if current volume is significantly above average.
    """
    try:
        vol_now = row.get("Volume", 0)
        vol_avg_3mo = row.get("3_Months_Volume", 0)

        if vol_now and vol_avg_3mo and vol_avg_3mo > 0:
            increase_pct = ((vol_now - vol_avg_3mo) / vol_avg_3mo) * 100
            return increase_pct >= threshold
        return False
    except:
        return False


def is_rvol_strong(row, min_rvol=1.5):
    """
    Uses RVOL to indicate trading activity vs. historical average.
    """
    try:
        rvol = row.get("RVOL", 0)
        return rvol >= min_rvol
    except:
        return False


def is_momentum_strong(row):
    """
    Quick check if recent returns indicate strong upside momentum.
    """
    try:
        return_7d = row.get("7_Days_Returns", 0)
        return_30d = row.get("30_Days_Returns", 0)

        return (return_7d > 2 and return_30d > 5)
    except:
        return False
