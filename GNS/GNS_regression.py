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


BTC_liquidation = pd.read_csv('/Users/andyma/Desktop/Python /Perpetual_futures/GNS/GNS_liquidation.csv', index_col=0)

############################# decomposing the expected and unexpected parts
### for liquidation long as the initation
adf_liquidation_long = adfuller(BTC_liquidation['liquidate_long'], autolag='AIC')
ADF={'liquidate_long':[adf_liquidation_long[0],adf_liquidation_long[1]]}
if adf_liquidation_long[1]<0.1:
    model_liquidation_long = auto_arima(BTC_liquidation['liquidate_long'], start_p=1, start_q=1, max_p=5, max_q=5,
                                        seasonal=False, d=0, D=0, trace=True, error_action='ignore',
                                        suppress_warnings=True, stepwise=True)
else:
    model_liquidation_long = auto_arima(BTC_liquidation['liquidate_long'], start_p=1, start_q=1, max_p=5, max_q=5,
                                        seasonal=False, d=1, D=0, trace=True, error_action='ignore',
                                        suppress_warnings=True, stepwise=True)
MRIMA_order={'liquidate_long':model_liquidation_long.order}
model_liquidation_long = ARIMA(BTC_liquidation['liquidate_long'], order=model_liquidation_long.order).fit()
fitted['liquidate_long']=model_liquidation_long.fittedvalues
residual['liquidate_long']=model_liquidation_long.resid
########################### define a function for subsequent data
def decompose(Var_name):
    adf = adfuller(BTC_liquidation[Var_name], autolag='AIC')
    ADF[Var_name]= [adf[0], adf[1]]
    if adf[1] < 0.1:
        model = auto_arima(BTC_liquidation[Var_name], start_p=1, start_q=1, max_p=5, max_q=5,
                                            seasonal=False, d=0, D=0, trace=True, error_action='ignore',
                                            suppress_warnings=True, stepwise=True)
    else:
        model = auto_arima(BTC_liquidation[Var_name], start_p=1, start_q=1, max_p=5, max_q=5,
                                            seasonal=False, d=1, D=0, trace=True, error_action='ignore',
                                            suppress_warnings=True, stepwise=True)
    MRIMA_order[Var_name]=model.order
    model = ARIMA(BTC_liquidation[Var_name], order=model.order).fit()
    fitted[Var_name] = model.fittedvalues
    residual[Var_name] = model.resid


### for liquidation short
decompose('liquidate_short')
### for leverage long
decompose('leverage_long')
### for leverage short
decompose('leverage_short')
### for trading volume
decompose('TradingVolume_usd')
### for open interest short
decompose('OpenInterest_short')
### for open interest long
decompose('OpenInterest_long')

### categories of leverage

# 1.1X - 5X
decompose('1.1X - 5X')
# 5X - 10X
decompose('5X - 10X')
# 10X - 15X
decompose('10X - 15X')
# 15X - 20X
decompose('15X - 20X')
# 20X - 25X
decompose('20X - 25X')
# 25X - 30X
decompose('25X - 30X')
# 30X - 35X
decompose('30X - 35X')
# 35X - 40X
decompose('35X - 40X')
# 40X - 45X
decompose('40X - 45X')
# 45X - 50X
decompose('45X - 50X')
# More than 50X
decompose('More than 50X')



############################# get the volitility
firstTerm_inside=0.5*(np.log(BTC_liquidation['high']/BTC_liquidation['low']))**2
secondTerm_inside=(2*np.log(2)-1)*(np.log(BTC_liquidation['open']/BTC_liquidation['close']))**2
sigma_hat=(firstTerm_inside-secondTerm_inside)**(1/2)

############################################### regression
####################### for average leverage
### build dependent var
y=pd.DataFrame()
y['sigma']=sigma_hat
y.drop(index=y.index[-1], axis=0, inplace=True)


### build independent var
X=pd.DataFrame()
# the lagged term of sigma
X['sigma_lag1']=sigma_hat.shift(-1)
# expected trading activity
X['E_OpenInterest_short']=fitted['OpenInterest_short']
X['E_OpenInterest_long']=fitted['OpenInterest_long']
X['E_trading_volume']=fitted['TradingVolume_usd']
# unexpected trading activity
X['U_OpenInterest_short']=residual['OpenInterest_short']
X['U_OpenInterest_long']=residual['OpenInterest_long']
X['U_trading_volume']=residual['TradingVolume_usd']

# expected liquidation & leverage
X['E_liquidate_short']=fitted['liquidate_short']
X['E_liquidate_long']=fitted['liquidate_long']
X['E_leverage_short']=fitted['leverage_short']
X['E_leverage_long']=fitted['leverage_long']
# unexpected liquidation & leverage
X['U_liquidate_short']=residual['liquidate_short']
X['U_liquidate_long']=residual['liquidate_long']
X['U_leverage_short']=residual['leverage_short']
X['U_leverage_long']=residual['leverage_long']
X = sm.add_constant(X)

X.drop(index=X.index[-1], axis=0, inplace=True)

lm = sm.OLS(y, X).fit()
print(lm.summary())

####################### for categories of leverage
### build dependent var
y1=pd.DataFrame()
y1['sigma']=sigma_hat
y1.drop(index=y1.index[-1], axis=0, inplace=True)


### build independent var
X1=pd.DataFrame()
# the lagged term of sigma
X1['sigma_lag1']=sigma_hat.shift(-1)
# expected trading activity
X1['E_OpenInterest_short']=fitted['OpenInterest_short']
X1['E_OpenInterest_long']=fitted['OpenInterest_long']
# X1['E_trading_volume']=fitted['TradingVolume_usd']
# unexpected trading activity
X1['U_OpenInterest_short']=residual['OpenInterest_short']
X1['U_OpenInterest_long']=residual['OpenInterest_long']
# X1['U_trading_volume']=residual['TradingVolume_usd']

# expected liquidation & leverage
X1['E_liquidate_short']=fitted['liquidate_short']
X1['E_liquidate_long']=fitted['liquidate_long']

X1['E_1X_5X']=fitted['1.1X - 5X']
X1['E_5X_10X']=fitted['5X - 10X']
X1['E_10X_15X']=fitted['10X - 15X']
X1['E_15X_20X']=fitted['15X - 20X']
X1['E_20X_25X']=fitted['20X - 25X']
X1['E_25X_30X']=fitted['25X - 30X']
X1['E_30X_35X']=fitted['30X - 35X']
X1['E_35X_40X']=fitted['35X - 40X']
X1['E_40X_45X']=fitted['40X - 45X']
X1['E_45X_50X']=fitted['45X - 50X']
X1['E_more than 50X']=fitted['More than 50X']

# unexpected liquidation & leverage
X1['U_liquidate_short']=residual['liquidate_short']
X1['U_liquidate_long']=residual['liquidate_long']

X1['U_1X_5X']=residual['1.1X - 5X']
X1['U_5X_10X']=residual['5X - 10X']
X1['U_10X_15X']=residual['10X - 15X']
X1['U_15X_20X']=residual['15X - 20X']
X1['U_20X_25X']=residual['20X - 25X']
X1['U_25X_30X']=residual['25X - 30X']
X1['U_30X_35X']=residual['30X - 35X']
X1['U_35X_40X']=residual['35X - 40X']
X1['U_40X_45X']=residual['40X - 45X']
X1['U_45X_50X']=residual['45X - 50X']
X1['U_more than 50X']=residual['More than 50X']

X1 = sm.add_constant(X1)

X1.drop(index=X1.index[-1], axis=0, inplace=True)

lm = sm.OLS(y1, X1).fit()
print(lm.summary())


######################## add the second lagged term of sigma (with larger AIC so we do not adopt it)
### build dependent var
y2=pd.DataFrame()
y2['sigma']=sigma_hat
y2.drop(y2.tail(2).index,inplace = True)

### build independent var
X2=pd.DataFrame()
# the lagged term of sigma
X2['sigma_lag1']=sigma_hat.shift(-1)
X2['sigma_lga2']=sigma_hat.shift(-2)
# expected trading activity
X2['E_OpenInterest_short']=fitted['OpenInterest_short']
X2['E_OpenInterest_long']=fitted['OpenInterest_long']
X2['E_trading_volume']=fitted['TradingVolume_usd']
# unexpected trading activity
X2['U_OpenInterest_short']=residual['OpenInterest_short']
X2['U_OpenInterest_long']=residual['OpenInterest_long']
X2['U_trading_volume']=residual['TradingVolume_usd']

# expected liquidation & leverage
X2['E_liquidate_short']=fitted['liquidate_short']
X2['E_liquidate_long']=fitted['liquidate_long']
X2['E_leverage_short']=fitted['leverage_short']
X2['E_leverage_long']=fitted['leverage_long']
# unexpected liquidation & leverage
X2['U_liquidate_short']=residual['liquidate_short']
X2['U_liquidate_long']=residual['liquidate_long']
X2['U_leverage_short']=residual['leverage_short']
X2['U_leverage_long']=residual['leverage_long']
X2 = sm.add_constant(X2)

X2.drop(X2.tail(2).index,inplace = True)

lm2 = sm.OLS(y2, X2).fit()
print(lm2.summary())



print(BTC_liquidation['leverage_long'].mean())
print(BTC_liquidation['leverage_short'].mean())
ttest=ttest_ind(BTC_liquidation['leverage_long'],BTC_liquidation['leverage_short'])