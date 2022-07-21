# coding: utf-8
"""Example 7.4"""
# Principal Component Analysis as an Example of Factor Model
import math
import numpy as np
import pandas as pd
from numpy.linalg import eig
from numpy.linalg import eigh

# from statsmodels.api import OLS
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.multioutput import MultiOutputRegressor
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn import linear_model
from sklearn.linear_model import Ridge
import time

lookback = 252  # training period for factor exposure
numFactors = 5
topN = 50  # for trading strategy, long stocks with topN exepcted 1-day returns

df = pd.read_table("miscFiles/IJR_20080114.txt")
df["Date"] = df["Date"].astype("int")
df.set_index("Date", inplace=True)
df.sort_index(inplace=True)
df.fillna(method="ffill", inplace=True)

dailyret = (
    df.pct_change()
)  # note the rows of dailyret are the observations at different time periods
positionsTable = np.zeros(df.shape)
end_index = df.shape[0]
# end_index = lookback + 10
for t in np.arange(lookback + 1, end_index):
    R = dailyret.iloc[
        t - lookback + 1 : t,
    ].T  # here the columns of R are the different observations.
    hasData = np.where(R.notna().all(axis=1))[0]
    R.dropna(inplace=True)  # avoid any stocks with missing returns
    pca = PCA()
    X = pca.fit_transform(R.T)[:, :numFactors]
    X = sm.add_constant(X)
    y1 = R.T
    clf = MultiOutputRegressor(LinearRegression(fit_intercept=False), n_jobs=4).fit(
        X, y1
    )
    Rexp = np.sum(clf.predict(X), axis=0)
    R = dailyret.iloc[
        t - lookback + 1 : t + 1,
    ].T  # here the columns of R are the different observations.

    idxSort = Rexp.argsort()

    positionsTable[t, hasData[idxSort[np.arange(0, topN)]]] = -1
    # positionsTable[t, hasData[idxSort[np.arange(-topN,0)]]]=1
    positionsTable[t, hasData[idxSort[np.arange(-topN, -1)]]] = 1

capital = np.nansum(np.array(abs(pd.DataFrame(positionsTable)).shift()), axis=1)
positionsTable[
    capital == 0,
] = 0
capital[capital == 0] = 1
ret = (
    np.nansum(
        np.array(pd.DataFrame(positionsTable).shift()) * np.array(dailyret), axis=1
    )
    / capital
)
avgret = np.nanmean(ret) * 252
avgstdev = np.nanstd(ret) * math.sqrt(252)
Sharpe = avgret / avgstdev
print(avgret)
print(avgstdev)
print(Sharpe)

# 0.04052422056844459
# 0.07002908500498846
# 0.5786769963588398
