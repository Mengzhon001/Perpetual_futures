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


BTC_liquidation = pd.read_csv('BTC_liquidation.csv', index_col=0)

BTC_liquidation['High_leverage']=BTC_liquidation[[ 'More than 50X']].sum(axis=1)
BTC_liquidation['Median_leverage']=BTC_liquidation[[ '5X - 10X', '10X - 15X', '15X - 20X', '20X - 25X','25X - 30X','30X - 35X', '35X - 40X','40X - 45X', '45X - 50X']].sum(axis=1)
BTC_liquidation['Low_leverage']=BTC_liquidation[['Less than 1.1X','1.1X - 5X']].sum(axis=1)

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

# low leverage
decompose('Low_leverage')
# high leverage
decompose('High_leverage')
# Median_leverage
decompose('Median_leverage')



############################# get the volitility
firstTerm_inside=0.5*(np.log(BTC_liquidation['high']/BTC_liquidation['low']))**2
secondTerm_inside=(2*np.log(2)-1)*(np.log(BTC_liquidation['open']/BTC_liquidation['close']))**2
sigma_hat=(firstTerm_inside-secondTerm_inside)**(1/2)

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
X1['E_Low_leverage']=fitted['Low_leverage']
X1['E_High_leverage']=fitted['High_leverage']
X1['E_Median_leverage']=fitted['Median_leverage']

# unexpected liquidation & leverage
X1['U_liquidate_short']=residual['liquidate_short']
X1['U_liquidate_long']=residual['liquidate_long']
X1['U_Low_leverage']=fitted['Low_leverage']
X1['U_High_leverage']=fitted['High_leverage']
X1['U_Median_leverage']=fitted['Median_leverage']

X1 = sm.add_constant(X1, has_constant='add')

X1.drop(index=X1.index[-1], axis=0, inplace=True)

lm = sm.OLS(y1, X1).fit()
print(lm.summary())