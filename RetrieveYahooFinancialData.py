from pandas_datareader import data as pdr
import numpy as np
import pandas as pd

"""Retrieve stock historical financial pricing information from Yahoo! Finance."""
appendedData = []
# Download Data from Yahoo
def test_yfinance(symbols, startDate, endDate):

    dataList = []
    for symbol in symbols:
        symbolData = pdr.get_data_yahoo(symbol, startDate, endDate)
        symbolData = symbolData.assign(Symbol=symbol)
        # Convert symbol dataframe data to list and append all symbols
        appendedData.append(symbolData)
    df = pd.concat(appendedData)
    df["Date"] = df.index
    # df.reset_index(inplace=True)
    df.set_index(["Symbol", "Date"], inplace=True)

    print(df)


if __name__ == "__main__":
    # if script called directly
    test_yfinance(
        ["AAPL", "MSFT", "VFINX", "BTC-USD"],
        startDate="2020-09-25",
        endDate="2020-10-02",
    )
