from calculateMaxDD import calculateMaxDD

"""Calculating Maximum Drawdown and Maximum Drawdown Duration"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import os

"""From Example 3-4"""
"""-----------------------------------"""
df = pd.read_excel("miscFiles/IGE.xls")
df.sort_values(by="Date", inplace=True)
dailyRet = df.loc[:, "Adj Close"].pct_change()  # daily returns
excessRet = dailyRet - 0.04 / 252
# excess daily returns = strategy return - financial cost, assuming risk free rate of return
sharpeRatio = np.sqrt(252) * np.mean(excessRet) / np.std(excessRet)
print(sharpeRatio)

df2 = pd.read_excel("miscFiles/SPY.xls")
df = pd.merge(df, df2, on="Date", suffixes=("_IGE", "_SPY"))
df["Date"] = pd.to_datetime(df["Date"])
df.set_index("Date", inplace=True)
df.sort_index(inplace=True)
dailyRet = df[["Adj Close_IGE", "Adj Close_SPY"]].pct_change()  # daily returns
dailyRet.rename(columns={"Adj Close_IGE": "IGE", "Adj Close_SPY": "SPY"}, inplace=True)
netRet = (dailyRet["IGE"] - dailyRet["SPY"]) / 2
sharpeRatio = np.sqrt(252) * np.mean(netRet) / np.std(netRet)
print(sharpeRatio)
"""-----------------------------------"""
cumRet = np.cumprod(1 + netRet) - 1
plt.plot(cumRet)

maxDrawdown, maxDrawdownDuration, startDrawdownDay = calculateMaxDD(cumRet.values)
print(maxDrawdown, maxDrawdownDuration, startDrawdownDay)
