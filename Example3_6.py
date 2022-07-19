"""
Example 3-6
# Pair Trading of GLD and GDX
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm


df1 = pd.read_excel("miscFiles/GLD.xls")
df2 = pd.read_excel("miscFiles/GDX.xls")
df = pd.merge(df1, df2, on="Date", suffixes=("_GLD", "_GDX"))
df.set_index("Date", inplace=True)
df.sort_index(inplace=True)

trainset = np.arange(0, 252)
testset = np.arange(trainset.shape[0], df.shape[0])

"""
## Determine hedge ratio on trainset
"""
model = sm.OLS(
    df.loc[:, "Adj Close_GLD"].iloc[trainset], df.loc[:, "Adj Close_GDX"].iloc[trainset]
)
results = model.fit()
hedgeRatio = results.params
print(hedgeRatio)

"""
##  spread = GLD - hedgeRatio*GDX
"""
spread = df.loc[:, "Adj Close_GLD"] - hedgeRatio[0] * df.loc[:, "Adj Close_GDX"]
plt.plot(spread.iloc[trainset])
plt.plot(spread.iloc[testset])
spreadMean = np.mean(spread.iloc[trainset])
print(spreadMean)

spreadStd = np.std(spread.iloc[trainset])
print(spreadStd)

df["zscore"] = (spread - spreadMean) / spreadStd
df["positions_GLD_Long"] = 0
df["positions_GDX_Long"] = 0
df["positions_GLD_Short"] = 0
df["positions_GDX_Short"] = 0
df.loc[df.zscore >= 2, ("positions_GLD_Short", "positions_GDX_Short")] = [
    -1,
    1,
]  # Short spread
df.loc[df.zscore <= -2, ("positions_GLD_Long", "positions_GDX_Long")] = [
    1,
    -1,
]  # Buy spread
df.loc[
    df.zscore <= 1, ("positions_GLD_Short", "positions_GDX_Short")
] = 0  # Exit short spread
df.loc[
    df.zscore >= -1, ("positions_GLD_Long", "positions_GDX_Long")
] = 0  # Exit long spread
df.fillna(
    method="ffill", inplace=True
)  # ensure existing positions are carried forward unless there is an exit signal
positions_Long = df.loc[:, ("positions_GLD_Long", "positions_GDX_Long")]
positions_Short = df.loc[:, ("positions_GLD_Short", "positions_GDX_Short")]
positions = np.array(positions_Long) + np.array(positions_Short)
positions = pd.DataFrame(positions)
dailyret = df.loc[:, ("Adj Close_GLD", "Adj Close_GDX")].pct_change()
pnl = (np.array(positions.shift()) * np.array(dailyret)).sum(axis=1)
sharpeTrainset = np.sqrt(252) * np.mean(pnl[trainset[1:]]) / np.std(pnl[trainset[1:]])
print(sharpeTrainset)


sharpeTestset = np.sqrt(252) * np.mean(pnl[testset]) / np.std(pnl[testset])
print(sharpeTestset)
plt.plot(np.cumsum(pnl[testset]))


positions.to_pickle("example3_6_positions")
