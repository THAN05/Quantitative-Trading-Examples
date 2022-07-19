"""
Example 7-2
# How to Form a Good Cointegrating (and Mean-Reverting) Pair of Stocks
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import coint
from statsmodels.api import OLS

df1 = pd.read_excel("miscFiles/GLD.xls")
df2 = pd.read_excel("miscFiles/GDX.xls")
df = pd.merge(df1, df2, on="Date", suffixes=("_GLD", "_GDX"))
df.set_index("Date", inplace=True)
df.sort_index(inplace=True)
trainset = np.arange(0, 252)
df = df.iloc[
    trainset,
]
"""
## Run cointegration (Engle-Granger) test
"""
coint_t, pvalue, crit_value = coint(df["Adj Close_GLD"], df["Adj Close_GDX"])
(
    coint_t,
    pvalue,
    crit_value,
)  # abs(t-stat) > critical value at 95%. pvalue says probability of null hypothesis (of no cointegration) is only 1.8%
"""
## Determine hedge ratio
"""
model = OLS(df["Adj Close_GLD"], df["Adj Close_GDX"])
results = model.fit()
hedgeRatio = results.params
print("Hedge Ratio")
print(hedgeRatio)
"""
##  spread = GLD - hedgeRatio*GDX
"""
spread = df["Adj Close_GLD"] - hedgeRatio[0] * df["Adj Close_GDX"]
print("Spread")
plt.plot(spread)
plt.show()