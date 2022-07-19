"""
Example 3-7
# Simple Mean-Reverting Model with and without Transaction Costs
"""
import numpy as np
import pandas as pd

startDate = 20060101
endDate = 20061231

df = pd.read_table("miscFiles/SPX_20071123.txt")
df["Date"] = df["Date"].astype("int")
df.set_index("Date", inplace=True)
df.sort_index(inplace=True)
dailyret = df.pct_change()

marketDailyret = dailyret.mean(axis=1)
weights = -(
    np.array(dailyret) - np.array(marketDailyret).reshape((dailyret.shape[0], 1))
)
wtsum = np.nansum(abs(weights), axis=1)

weights[
    wtsum == 0,
] = 0
wtsum[wtsum == 0] = 1
weights = weights / wtsum.reshape((dailyret.shape[0], 1))


dailypnl = np.nansum(
    np.array(pd.DataFrame(weights).shift()) * np.array(dailyret), axis=1
)
dailypnl = dailypnl[np.logical_and(df.index >= startDate, df.index <= endDate)]
sharpeRatio = np.sqrt(252) * np.mean(dailypnl) / np.std(dailypnl)

print(sharpeRatio)

"""
# With transaction costs
"""
onewaytcost = 0.0005
weights = weights[np.logical_and(df.index >= startDate, df.index <= endDate)]
dailypnlminustcost = dailypnl - (
    np.nansum(abs(weights - np.array(pd.DataFrame(weights).shift())), axis=1)
    * onewaytcost
)
sharpeRatioMinusTcost = (
    np.sqrt(252) * np.mean(dailypnlminustcost) / np.std(dailypnlminustcost)
)
print(sharpeRatioMinusTcost)
