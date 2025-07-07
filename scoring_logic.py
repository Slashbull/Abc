# scoring_logic.py

def score_stock(row):
    try:
        # Defensive defaults
        price = row.get("Current_Price", None)
        pe = row.get("PE", None)
        eps_growth = row.get("EPS_Change", None)
        pct_from_low = row.get("Pct_From_Low", None)
        pct_from_high = row.get("Pct_From_High", None)
        rvol = row.get("RVOL", None)
        dma_20 = row.get("20_Day_Avg", None)
        dma_200 = row.get("200_Day_Avg", None)
        ret_1yr = row.get("1_Year", None)

        # Basic condition: strong price action and volume
        if (
            price and rvol and pct_from_low is not None and
            price > dma_200 and
            pct_from_low < 20 and
            pct_from_high < 10 and
            rvol > 1
        ):
            return "BUY"

        # Watch condition: Near breakout or forming base
        elif (
            price and dma_20 and dma_200 and
            abs(price - dma_20) / dma_20 < 0.05 and
            abs(price - dma_200) / dma_200 < 0.1 and
            ret_1yr is not None and ret_1yr > 0
        ):
            return "WATCH"

        # Everything else is avoid for now
        else:
            return "AVOID"

    except Exception as e:
        print("Scoring error:", e)
        return "AVOID"
