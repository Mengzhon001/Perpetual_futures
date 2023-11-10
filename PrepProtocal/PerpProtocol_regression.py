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


BTC_liquidation = pd.read_csv('/Users/andyma/Desktop/Python /Perpetual_futures/PrepProtocal/PrepProtocal_finalData.csv', index_col=0)

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
### for trading volume
decompose('TradingVolume_usd')
### for open interest short
decompose('OpenInterest_short')
### for open interest long
decompose('OpenInterest_long')



############################# get the volitility
firstTerm_inside=0.5*(np.log(BTC_liquidation['high']/BTC_liquidation['low']))**2
secondTerm_inside=(2*np.log(2)-1)*(np.log(BTC_liquidation['open']/BTC_liquidation['close']))**2
sigma_hat=(firstTerm_inside-secondTerm_inside)**(1/2)

############################################### regression

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
# expected liquidation
X['E_liquidate_short']=fitted['liquidate_short']
X['E_liquidate_long']=fitted['liquidate_long']
# unexpected liquidation & leverage
X['U_liquidate_short']=residual['liquidate_short']
X['U_liquidate_long']=residual['liquidate_long']

X = sm.add_constant(X)

X.drop(index=X.index[-1], axis=0, inplace=True)

lm = sm.OLS(y, X).fit()
print(lm.summary())

####################### for IS and LIQ

### build dependent var
y=pd.DataFrame()
y['sigma']=sigma_hat
y.drop(index=y.index[-1], axis=0, inplace=True)


### build independent var
X=pd.DataFrame()
# the lagged term of sigma
X['sigma_lag1']=sigma_hat.shift(-1)
# trading activity
X['OpenInterest_short']=BTC_liquidation['OpenInterest_short']
X['OpenInterest_long']=BTC_liquidation['OpenInterest_long']
X['trading_volume']=BTC_liquidation['TradingVolume_usd']
# SI and LIQ
X['SI']=(BTC_liquidation['TradingVolume_usd'])/((BTC_liquidation['OpenInterest_long']+BTC_liquidation['OpenInterest_long'])/2)
X['LIQ_long']=BTC_liquidation['liquidate_long']/BTC_liquidation['OpenInterest_long']
X['LIQ_short']=BTC_liquidation['liquidate_short']/BTC_liquidation['OpenInterest_short']


X = sm.add_constant(X, has_constant='add')

X.drop(index=X.index[-1], axis=0, inplace=True)

lm = sm.OLS(y, X).fit()
print(lm.summary())