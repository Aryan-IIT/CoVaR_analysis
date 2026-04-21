import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# -------------------------------
# Dynamic 2-year range
# -------------------------------
end_date = datetime.today()
start_date = end_date - timedelta(days=730)

start_date = start_date.strftime("%Y-%m-%d")
end_date = end_date.strftime("%Y-%m-%d")


def fetch_and_save(ticker, file_name):
    data = yf.download(
        ticker,
        start=start_date,
        end=end_date,
        auto_adjust=False
    )

    # Fix MultiIndex issue (important)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = ['_'.join(col).strip() for col in data.columns.values]

    data.reset_index(inplace=True)
    data.to_excel(file_name, index=False)

    print(f"{ticker} saved to {file_name}")


# -------------------------------
# Market + Risk Profile Set
# -------------------------------
fetch_and_save("^NSEI", "nifty50_2years.xlsx")
fetch_and_save("HINDUNILVR.NS", "hul_2years.xlsx")
fetch_and_save("ADANIENT.NS", "adani_enterprises_2years.xlsx")


# -------------------------------
# Sector Trio
# -------------------------------
fetch_and_save("HDFCBANK.NS", "hdfc_bank_2years.xlsx")
fetch_and_save("TCS.NS", "tcs_2years.xlsx")