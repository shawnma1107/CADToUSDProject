import yfinance as yf
import pandas as pd

def run():
    data = yf.download(tickers='USDCAD=X', start='2020-04-01', end='2025-03-31', auto_adjust=True)
    pd.set_option('display.max_rows', None)
    data = data[['Close']]
    data.to_csv("data/exchange_rate.csv")

if __name__ == "__main__":
    run()
