from pandas_datareader import data as pdr

"""Retrieve stock historical financial pricing information from Yahoo! Finance."""

# Example 3.1: Download Data from Yahoo
def test_yfinance():
    for symbol in ["AAPL", "MSFT", "VFINX", "BTC-USD"]:
        print(">>", symbol, end=" ... ")
        data = pdr.get_data_yahoo(symbol, start="2020-09-25", end="2020-10-02")
        print(data)


if __name__ == "__main__":
    # if script called directly
    test_yfinance()
