import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import grangercausalitytests
from statsmodels.tsa.stattools import adfuller


transaction=pd.read_csv('/Users/andyma/Desktop/Python /Perpetual_futures/BTCprice_LP/LP_transactions.csv')
transaction['DateTime']=transaction['DateTime'].str.split(pat=' ', expand=True)[0]

Grouped_trans=transaction.groupby(['DateTime','Txhash'])['To'].apply('_'.join).reset_index()

trans_add=Grouped_trans[Grouped_trans['To']=='0xc64f9436f8ca50cdcc096105c62dad52faeb1f2e_0xc64f9436f8ca50cdcc096105c62dad52faeb1f2e'].reset_index()
trans_add.drop(['index','To'],axis='columns', inplace=True)

trans_remove=Grouped_trans[Grouped_trans['To']=='0x82ac2ce43e33683c58be4cdc40975e73aa50f459_0x82ac2ce43e33683c58be4cdc40975e73aa50f459'].reset_index()
trans_remove.drop(['index','To'],axis='columns', inplace=True)

tx_value=transaction[['Txhash','TokenValue','TokenSymbol']]
tx_usd=tx_value[tx_value['TokenSymbol']=='vUSD']
tx_btc=tx_value[tx_value['TokenSymbol']=='vBTC']

Daily_add_trans=pd.merge(trans_add, tx_btc , how="left", on="Txhash")
Daily_add_trans['TokenValue'] = Daily_add_trans['TokenValue'].astype(float)
Daily_add=Daily_add_trans.groupby(['DateTime'],as_index=False)['TokenValue'].sum()

Daily_remove_trans=pd.merge(trans_remove, tx_btc, how="left", on="Txhash")
Daily_remove_trans['TokenValue'] = Daily_remove_trans['TokenValue'].astype(float)
Daily_remove=Daily_remove_trans.groupby(['DateTime'],as_index=False)['TokenValue'].sum()

##################### load the btc pricing data
BTC_OHLC=pd.read_csv('/BTC_pricing/BTC_OHLC_data.csv', index_col=0)
BTC_OHLC['time'] = pd.to_datetime(BTC_OHLC['time'],unit='s')
BTC_OHLC['time']=BTC_OHLC['time'].astype('string').str.split(pat=' ', expand=True)[0]
BTC_OHLC=BTC_OHLC.drop(['volumefrom','volumeto','conversionType','conversionSymbol'], axis=1)

BTC_OHLC=BTC_OHLC[BTC_OHLC['time']>='2023-05-15']
BTC_OHLC=BTC_OHLC[BTC_OHLC['time']<='2023-10-15']
BTC_OHLC.drop(['high','low'],axis='columns', inplace=True)

BTC_OHLC['Return']=np.log(BTC_OHLC['close'])-np.log(BTC_OHLC['open'])
BTC_OHLC.drop(['close'],axis='columns', inplace=True)
BTC_OHLC.rename(columns = {'time':'DateTime'}, inplace = True)

################### merge
final_data=pd.merge(BTC_OHLC, Daily_add , how="left", on="DateTime")
final_data=pd.merge(final_data, Daily_remove , how="left", on="DateTime")
final_data=final_data.fillna(0)

final_data['net_change_liquidity']=final_data['TokenValue_x']-final_data['TokenValue_y']

final_data=final_data[final_data['net_change_liquidity'] != 0]

print(grangercausalitytests(final_data[['net_change_liquidity', 'Return']], maxlag=[15]))
print(grangercausalitytests(final_data[['Return','net_change_liquidity']], maxlag=[15]))

