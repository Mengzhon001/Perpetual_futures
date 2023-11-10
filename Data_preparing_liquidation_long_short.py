import numpy as np
import pandas as pd

### load and process liquidation data
data_liquidation=pd.read_csv('/Users/andyma/Desktop/Projects/Roger/Data/GMX_WBTC_liquidation.csv',index_col=0)
data_liquidation_daily=data_liquidation.groupby(['time','trade'],as_index=False)['volume_usd'].sum()
data_liquidation_daily['time']=data_liquidation_daily['time'].str.split(pat=' ', expand=True)[0]
data_liquidation_daily=data_liquidation_daily.pivot(index='time',columns='trade',values='volume_usd').reset_index()


#### load the BTC pricing data
BTC_OHLC=pd.read_csv('/Users/andyma/Desktop/Python /Perpetual_futures/BTC_OHLC_data.csv',index_col=0)
BTC_OHLC['time'] = pd.to_datetime(BTC_OHLC['time'],unit='s')
BTC_OHLC['time']=BTC_OHLC['time'].astype('string').str.split(pat=' ', expand=True)[0]

################################### process the trading volume data
data_volume=pd.read_csv('/Users/andyma/Desktop/Projects/Roger/Data/GMX_WBTC_tradingVolume.csv',index_col=0)
data_volume['time']=data_volume['time'].str.split(pat=' ', expand=True)[0]

################################### load and process open interest
data_openInterest=pd.read_csv('/Users/andyma/Desktop/Projects/Roger/Data/GMX_WBTC_open_interest.csv',index_col=0)
data_openInterest['time']=data_openInterest['time'].astype('string').str.split(pat=' ', expand=True)[0]
data_openInterest_daily=data_openInterest[['time','short','long']]
data_openInterest_daily.rename(columns = {'short':'OpenInterest_short','long':'OpenInterest_long'}, inplace = True)


################################### load and process leverage data
data_leverage=pd.read_csv('/Users/andyma/Desktop/Projects/Roger/Data/GMX_WBTC_leverage.csv',index_col=0)
data_leverage.drop(['btcprice'],axis=1,inplace=True)
data_leverage.rename(columns = {'day':'time'}, inplace = True)
data_leverage['time']=data_leverage['time'].astype('string').str.split(pat=' ', expand=True)[0]

################################### load and process leverage (categories)
data_leverage_categories=pd.read_csv('/Users/andyma/Desktop/Projects/Roger/Data/GMX_WBTC_leverage_categories.csv',index_col=0)
data_leverage_categories.drop(['trader','transaction','collateral','fee'],axis=1,inplace=True)
data_leverage_categories.rename(columns = {'day':'time'}, inplace = True)
data_leverage_categories['time']=data_leverage_categories['time'].astype('string').str.split(pat=' ', expand=True)[0]
data_leverage_categories=data_leverage_categories.pivot(index='time',columns='leverage',values='volume').reset_index()
data_leverage_categories=data_leverage_categories.fillna(0)

### merge the BTC pricng data and the liquidation data
BTC_liquidation = pd.merge(data_volume,BTC_OHLC,how="left", on="time")
BTC_liquidation = pd.merge(BTC_liquidation, data_liquidation_daily,how="left", on="time")
BTC_liquidation = pd.merge(BTC_liquidation, data_openInterest_daily,how="left", on="time")
BTC_liquidation = pd.merge(BTC_liquidation, data_leverage,how="left", on="time")
BTC_liquidation = pd.merge(BTC_liquidation, data_leverage_categories,how="left", on="time")


BTC_liquidation=BTC_liquidation.drop(['volumefrom','volumeto','conversionType','conversionSymbol'], axis=1)

### output data
BTC_liquidation.rename(columns = {'liquidate-long':'liquidate_long','liquidate-short':'liquidate_short'}, inplace = True)
BTC_liquidation_Leverage = BTC_liquidation.loc[BTC_liquidation['time']<='2023-09-26',:]
BTC_liquidation_Leverage = BTC_liquidation_Leverage.reset_index(drop = True)
BTC_liquidation_Leverage=BTC_liquidation_Leverage.set_index('time')
BTC_liquidation_Leverage[['liquidate_long','liquidate_short']]=BTC_liquidation_Leverage[['liquidate_long','liquidate_short']].fillna(0)
BTC_liquidation_Leverage = BTC_liquidation_Leverage.dropna(subset=['leverage_long'])
BTC_liquidation_Leverage.sort_values(['time'],ascending=True,inplace=True)

BTC_liquidation_Leverage.to_csv('BTC_liquidation.csv')





