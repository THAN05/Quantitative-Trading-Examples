import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import os

"""Calculate Sharpe Ratio for Long-Only Vs. Marker Neutral Stratigies."""
df = pd.read_excel("miscFiles/IGE.xls")
df.sort_values(by="Date", inplace=True)
dailyRet = df.loc[:, "Adj Close"].pct_change()  # daily returns
excessRet = dailyRet - 0.04 / 252
# excess daily returns = strategy return - financial cost, assuming risk free rate of return
sharpeRatio = np.sqrt(252) * np.mean(excessRet) / np.std(excessRet)
print(sharpeRatio)
