"""
# How to Form a Good Cointegrating (and Mean-Reverting) Pair of Stocks
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import coint
from statsmodels.api import OLS
from scipy.stats import pearsonr

df1 = pd.read_excel("miscFiles/KO.xls")
df2 = pd.read_excel("miscFiles/PEP.xls")
df = pd.merge(df1, df2, on="Date", suffixes=("_KO", "_PEP"))
df.set_index("Date", inplace=True)
df.sort_index(inplace=True)
"""
## Run cointegration (Engle-Granger) test
"""
coint_t, pvalue, crit_value = coint(df["Adj Close_KO"], df["Adj Close_PEP"])
(
    coint_t,
    pvalue,
    crit_value,
)  # abs(t-stat) < critical value at 90%. pvalue says probability of null hypothesis (of no cointegration) is 73%
"""
## Determine hedge ratio
"""
model = OLS(df["Adj Close_KO"], df["Adj Close_PEP"])
results = model.fit()
hedgeRatio = results.params
print(hedgeRatio)
"""
##  spread = KO - hedgeRatio*PEP
"""
spread = df["Adj Close_KO"] - hedgeRatio[0] * df["Adj Close_PEP"]
plt.plot(spread)  # Figure 7.2
plt.show()
"""
## Correlation test
"""
dailyret = df.loc[:, ("Adj Close_KO", "Adj Close_PEP")].pct_change()
dailyret.corr()
dailyret_clean = dailyret.dropna()
pearsonr(
    dailyret_clean.iloc[:, 0], dailyret_clean.iloc[:, 1]
)  # first output is correlation coefficient, second output is pvalue.
