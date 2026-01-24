import logging
import yfinance as yf
import pandas as pd


def get_data(ticker: str) -> pd.DataFrame:
    df = yf.download(ticker, period="4y", interval="1d", auto_adjust=True)
    logging.debug(df.columns)

    return df[["Close", "Date"]]


if __name__ == "__main__":
    print(get_data("AAPL"))
