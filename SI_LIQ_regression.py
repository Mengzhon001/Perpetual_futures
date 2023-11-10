import pandas as pd
from pmdarima.arima import auto_arima
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pylab as plt
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from scipy.stats import ttest_ind

fitted=pd.DataFrame()
residual=pd.DataFrame()


BTC_liquidation = pd.read_csv('/Users/andyma/Desktop/Python /Perpetual_futures/Bybit/Bybit_finalData.csv', index_col=0)
BTC_liquidation.fillna(0, inplace=True)

SI=pd.read_csv('SI_measures.csv')
LIQ_long=pd.read_csv('LIQ_long.csv')
LIQ_short=pd.read_csv('LIQ_short.csv')



############################# get the volitility
firstTerm_inside=0.5*(np.log(BTC_liquidation['high']/BTC_liquidation['low']))**2
secondTerm_inside=(2*np.log(2)-1)*(np.log(BTC_liquidation['open']/BTC_liquidation['close']))**2
sigma_hat=(firstTerm_inside-secondTerm_inside)**(1/2)

############################################### regression



def SI_LIQ_reg(exchange):
    y = pd.DataFrame()
    y['sigma'] = sigma_hat
    y.drop(index=y.index[-1], axis=0, inplace=True)
    y.reset_index(drop=True,inplace=True)

    ### build independent var
    X = pd.DataFrame()
    # the lagged term of sigma
    X['sigma_lag1'] = sigma_hat.shift(-1)
    # expected trading activity
    X['SI_'+exchange] = SI['SI_'+exchange]
    X['LIQ_long_'+exchange] = LIQ_long['LIQ_long_'+exchange]
    X['LIQ_short_' + exchange] = LIQ_short['LIQ_short_' + exchange]

    X = sm.add_constant(X, has_constant='add')

    X.drop(index=X.index[-1], axis=0, inplace=True)
    X.reset_index(drop=True,inplace=True)

    X_nan_index=np.where(X.isna().any(axis=1))[0]
    y=y.drop(X_nan_index)
    X=X.drop(X_nan_index)

    lm = sm.OLS(y, X).fit()
    print(lm.summary())
    pass

SI_LIQ_reg('perp')


