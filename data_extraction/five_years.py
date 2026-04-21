import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# 5-year range
end_date = datetime.today()
start_date = end_date - timedelta(days=5*365)

def fetch_daily_data(ticker, file_name):
    data = yf.download(
        ticker,
        start=start_date,
        end=end_date,
        auto_adjust=True
    )

    # Fix MultiIndex columns
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = ['_'.join(col).strip() for col in data.columns.values]

    data.reset_index(inplace=True)

    # 🔥 Find correct Close column dynamically
    close_col = [col for col in data.columns if "Close" in col][0]

    # Calculate returns
    data["Daily Return"] = data[close_col].pct_change()

    # Save
    data.to_excel(file_name, index=False)

    print(f"{ticker} saved to {file_name}")


# Run
fetch_daily_data("HINDUNILVR.NS", "hul_5yr_daily.xlsx")
fetch_daily_data("HDFCBANK.NS", "hdfc_5yr_daily.xlsx")
fetch_daily_data("TCS.NS", "tcs_5yr_daily.xlsx")