import json
import requests
import pandas as pd
import io

############# load transactions data
params = {
  "format": "csv"
}
r = requests.get('https://api.dune.com/api/v1/query/2675565/results/csv?api_key=H9rqlaFKqoEQqA4DIHiTgmuUbDOpgWYP', params=params)
r = r.content
GNS_transaction = pd.read_csv(io.StringIO(r.decode('utf-8')))

GNS_transaction.rename(columns = {'day':'time'}, inplace = True)
GNS_transaction['time']=GNS_transaction['time'].astype('string').str.split(pat=' ', expand=True)[0]

a=GNS_transaction['type'].unique()

########################### daily data for liquidation
GNS_liquidation=GNS_transaction[GNS_transaction['type']=='Liquidation']
GNS_liquidation_daily=GNS_liquidation.groupby(['time','direction'],as_index=False)['position_size_dai'].sum()
GNS_liquidation_daily=GNS_liquidation_daily.pivot(index='time',columns='direction',values='position_size_dai').reset_index()
GNS_liquidation_daily=GNS_liquidation_daily.fillna(0)
GNS_liquidation_daily.rename(columns = {'long':'liquidate_long','short':'liquidate_short'}, inplace = True)


# dai is the stablecoin of USD

########################### daily data for open interest
params = {
  "format": "csv"
}
r = requests.get('https://api.dune.com/api/v1/query/2652711/results/csv?api_key=H9rqlaFKqoEQqA4DIHiTgmuUbDOpgWYP', params=params)
r = r.content
GNS_openInterest = pd.read_csv(io.StringIO(r.decode('utf-8')))

GNS_openInterest['time']=GNS_openInterest['time'].astype('string').str.split(pat=' ', expand=True)[0]
GNS_openInterest.drop(['long_format'],axis=1,inplace=True)
GNS_openInterest.drop(['short_format'],axis=1,inplace=True)
GNS_openInterest.drop(['delta_volume'],axis=1,inplace=True)
GNS_openInterest.rename(columns = {'long_volume':'OpenInterest_long','short_volume':'OpenInterest_short'}, inplace = True)

########################### daily trading volume
GNS_tradingVolume=GNS_transaction.groupby(['time'],as_index=False)['position_size_dai'].sum()
GNS_tradingVolume.rename(columns = {'position_size_dai':'TradingVolume_usd'}, inplace = True)

########################### daily average leverage
GNS_leverage_long=GNS_transaction[GNS_transaction['direction']=='long'].groupby(['time'],as_index=False)['leverage'].mean()
GNS_leverage_short=GNS_transaction[GNS_transaction['direction']=='short'].groupby(['time'],as_index=False)['leverage'].mean()
GNS_leverage_long.rename(columns = {'leverage':'leverage_long'}, inplace = True)
GNS_leverage_short.rename(columns = {'leverage':'leverage_short'}, inplace = True)

########################### categories of leverage
GNS_leverage_category=GNS_transaction[GNS_transaction['leverage']<1].groupby(['time'],as_index=False)['position_size_dai'].mean()
GNS_leverage_category.rename(columns = {'position_size_dai':'Less than 1.1X'}, inplace = True)

def category_leverage(lower_bound,GNS_leverage_category):
  upper_bound=lower_bound+5
  GNS_leverage_category_i = \
  GNS_transaction[(GNS_transaction['leverage'] < upper_bound) & (GNS_transaction['leverage'] >= lower_bound)].groupby(['time'],
                                                                                                    as_index=False)[
    'position_size_dai'].mean()
  GNS_leverage_category_i.rename(columns={'position_size_dai': str(lower_bound)+'X - '+str(upper_bound)+'X'}, inplace=True)
  GNS_leverage_category = pd.merge(GNS_leverage_category, GNS_leverage_category_i, how="outer", on="time")
  return GNS_leverage_category
  pass

GNS_leverage_category=category_leverage(1,GNS_leverage_category)
GNS_leverage_category=category_leverage(5,GNS_leverage_category)
GNS_leverage_category=category_leverage(10,GNS_leverage_category)
GNS_leverage_category=category_leverage(15,GNS_leverage_category)
GNS_leverage_category=category_leverage(20,GNS_leverage_category)
GNS_leverage_category=category_leverage(25,GNS_leverage_category)
GNS_leverage_category=category_leverage(30,GNS_leverage_category)
GNS_leverage_category=category_leverage(35,GNS_leverage_category)
GNS_leverage_category=category_leverage(40,GNS_leverage_category)
GNS_leverage_category=category_leverage(45,GNS_leverage_category)

GNS_leverage_category_more_than_50 = \
  GNS_transaction[ GNS_transaction['leverage'] >= 50].groupby(
    ['time'],
    as_index=False)[
    'position_size_dai'].mean()
GNS_leverage_category_more_than_50.rename(columns={'position_size_dai': 'More than 50X'},
                               inplace=True)
GNS_leverage_category = pd.merge(GNS_leverage_category, GNS_leverage_category_more_than_50, how="outer", on="time")

GNS_leverage_category=GNS_leverage_category.fillna(0)

GNS_leverage_category.rename(columns = {'1X - 6X':'1.1X - 5X'}, inplace = True)

############################### load the BTC pricing data
BTC_OHLC=pd.read_csv('/Users/andyma/Desktop/Python /Perpetual_futures/BTC_OHLC_data.csv',index_col=0)
BTC_OHLC['time'] = pd.to_datetime(BTC_OHLC['time'],unit='s')
BTC_OHLC['time']=BTC_OHLC['time'].astype('string').str.split(pat=' ', expand=True)[0]
BTC_OHLC=BTC_OHLC.drop(['volumefrom','volumeto','conversionType','conversionSymbol'], axis=1)


############################### merge
GNS_liquidation_data=pd.merge(BTC_OHLC, GNS_liquidation_daily, how="outer", on="time")
GNS_liquidation_data=pd.merge(GNS_liquidation_data, GNS_tradingVolume, how="outer", on="time")
GNS_liquidation_data=pd.merge(GNS_liquidation_data, GNS_openInterest, how="outer", on="time")
GNS_liquidation_data=pd.merge(GNS_liquidation_data, GNS_leverage_long, how="outer", on="time")
GNS_liquidation_data=pd.merge(GNS_liquidation_data, GNS_leverage_short, how="outer", on="time")
GNS_liquidation_data=pd.merge(GNS_liquidation_data, GNS_leverage_category, how="outer", on="time")

############################### trucate the data
GNS_liquidation_Leverage = GNS_liquidation_data.loc[4549:4718,:]
GNS_liquidation_Leverage=GNS_liquidation_Leverage.fillna(0)
GNS_liquidation_Leverage.to_csv('/Users/andyma/Desktop/Python /Perpetual_futures/GNS/GNS_liquidation.csv')