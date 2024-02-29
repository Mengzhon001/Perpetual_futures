import json
import requests
import pandas as pd
import io

############# load transactions data
Prep_transaction1=pd.read_csv('/Users/andyma/Desktop/Projects/Roger/Data_perpetualProtocol/20170101_20230101.csv')
Prep_transaction2=pd.read_csv('/Users/andyma/Desktop/Projects/Roger/Data_perpetualProtocol/20230102_20230926.csv')
Prep_transaction=pd.concat([Prep_transaction1, Prep_transaction2])



# Prep_transaction.rename(columns = {'day':'time'}, inplace = True)
Prep_transaction['time']=Prep_transaction['day'].str.split(pat=' ', expand=True)[0]
Prep_transaction['hour_min_sec']=Prep_transaction['day'].str.split(pat=' ', expand=True)[1]
Prep_transaction=Prep_transaction.drop('day',axis=1)
Prep_transaction.sort_values(['time','hour_min_sec'],ascending=True,inplace=True)


############# daily open interest constructing

### calculate the last trasactions per day per trader
idx = Prep_transaction.groupby(['time','trader_address'])['hour_min_sec'].transform(max) == Prep_transaction['hour_min_sec']
transactions_traderLast=Prep_transaction[idx]

transactions_traderLast['open_notional_abs']=transactions_traderLast['open_notional'].abs()
idx_abs=transactions_traderLast.groupby(['trader_address','time'])['open_notional_abs'].transform(max) == transactions_traderLast['open_notional_abs']
transactions_traderLast2=transactions_traderLast[idx_abs]

### sum the last transactions
# create var that is 'short' if ('open_notional<0') otherwise 'long'
transactions_traderLast2.loc[(transactions_traderLast2.open_notional > 0) ,'position_direction'] = 'long'
transactions_traderLast2.loc[(transactions_traderLast2.open_notional < 0) ,'position_direction'] = 'short'
transactions_traderLast2.dropna(subset=['position_direction'],inplace=True)
transactions_traderLast2 = transactions_traderLast2.reset_index(drop=True)


# for all the traders, update their positions each day to find the open interest everyday
trader_list=list(transactions_traderLast2['trader_address'].unique())

trader_position = pd.DataFrame(trader_list, columns=['trader_address'])
trader_position.set_index('trader_address',inplace=True)
trader_position['long']=0
trader_position['short']=0

date_list=list(transactions_traderLast2['time'].unique())
openInterest_daily = pd.DataFrame(date_list, columns=['time'])
openInterest_daily['long']=0
openInterest_daily['short']=0

### loop through the days to calculate the positions for all traders everyday
for d in date_list:
    print(d)
    transactions_Last_d = transactions_traderLast2[transactions_traderLast2['time'] == d]
    transactions_Last_d = transactions_Last_d[['trader_address', 'open_notional']]
    # process the duplicates in transactions for one trader
    transactions_Last_d['open_notional'] = transactions_Last_d.groupby(['trader_address'])['open_notional'].transform(
        'sum')
    transactions_Last_d.loc[(transactions_Last_d.open_notional > 0), 'position_direction'] = 'long'
    transactions_Last_d.loc[(transactions_Last_d.open_notional < 0), 'position_direction'] = 'short'
    transactions_Last_d.drop_duplicates(subset='trader_address', keep="first",inplace=True)
    ###
    transactions_Last_d = transactions_Last_d.pivot(index='trader_address', columns='position_direction',
                                                    values='open_notional').reset_index()
    transactions_Last_d.set_index('trader_address', inplace=True)
    transactions_Last_d.fillna(0, inplace=True)

    trader_position.update(transactions_Last_d)
    position_d = trader_position.sum()

    openInterest_daily.loc[openInterest_daily['time'] == d, 'long'] = position_d['long']
    openInterest_daily.loc[openInterest_daily['time'] == d, 'short'] = position_d['short']
    pass
openInterest_daily['short']=openInterest_daily['short'].abs()
openInterest_daily.rename(columns = {'long':'OpenInterest_long','short':'OpenInterest_short'}, inplace = True) # so the resulting df represents the dollar amount of liquidated position


############# daily liquidation constructing
liquidation_daily=Prep_transaction[Prep_transaction['liq_tx_or_not']==1].groupby(['time','direction'],as_index=False)['exchanged_position_notional'].sum()
liquidation_daily = liquidation_daily.pivot(index='time', columns='direction',values='exchanged_position_notional').reset_index()
liquidation_daily_t = pd.DataFrame(date_list, columns=['time'])
liquidation_daily=pd.merge(liquidation_daily_t, liquidation_daily, how="left", on="time")
liquidation_daily.fillna(0, inplace=True)
liquidation_daily['short']=liquidation_daily['short'].abs()
liquidation_daily.rename(columns = {'long':'liquidate_short','short':'liquidate_long'}, inplace = True) # so the resulting df represents the dollar amount of liquidated position

############# daily trading volume
Prep_transaction['exchanged_position_abs']=Prep_transaction['exchanged_position_notional'].abs()
tradingVolume_daily=Prep_transaction.groupby(['time'],as_index=False)['exchanged_position_abs'].sum()
tradingVolume_daily.rename(columns = {'exchanged_position_abs':'TradingVolume_usd'}, inplace = True) # so the resulting df represents the dollar amount of liquidated position

############# load BTC pricing data
BTC_OHLC=pd.read_csv('/BTC_pricing/BTC_OHLC_data.csv', index_col=0)
BTC_OHLC['time'] = pd.to_datetime(BTC_OHLC['time'],unit='s')
BTC_OHLC['time']=BTC_OHLC['time'].astype('string').str.split(pat=' ', expand=True)[0]
BTC_OHLC=BTC_OHLC.drop(['volumefrom','volumeto','conversionType','conversionSymbol'], axis=1)

############# merge the data
PerpProtocol_finalData = pd.merge(openInterest_daily, tradingVolume_daily,how="left", on="time")
PerpProtocol_finalData = pd.merge(PerpProtocol_finalData, liquidation_daily,how="left", on="time")
PerpProtocol_finalData = pd.merge(PerpProtocol_finalData, BTC_OHLC,how="left", on="time")

PerpProtocol_finalData.to_csv('/Users/andyma/Desktop/Python /Perpetual_futures/PrepProtocal/PrepProtocal_finalData.csv')

########### open interest calculating test
# transactions_Last_d=transactions_traderLast2[transactions_traderLast2['time']=='2021-11-27']
# transactions_Last_d=transactions_Last_d[['trader_address','open_notional']]
#
# transactions_Last_d['open_notional'] = transactions_Last_d.groupby(['trader_address'])['open_notional'].transform('sum')
# transactions_Last_d.loc[(transactions_Last_d.open_notional > 0) ,'position_direction'] = 'long'
# transactions_Last_d.loc[(transactions_Last_d.open_notional < 0) ,'position_direction'] = 'short'
#
#
# transactions_Last_d=transactions_Last_d.pivot(index='trader_address',columns='position_direction',values='open_notional').reset_index()
# transactions_Last_d.set_index('trader_address',inplace=True)
# transactions_Last_d.fillna(0,inplace=True)
#
# trader_position.update(transactions_Last_d)
# position_d=trader_position.sum()
#
# openInterest_daily.loc[openInterest_daily['time']=='2021-11-27','long']=position_d['long']
# openInterest_daily.loc[openInterest_daily['time']=='2021-11-27','short']=position_d['short']





# OpenInterest_daily=transactions_traderLast2.groupby(['time','position_direction'],as_index=False)['open_notional'].sum()
# OpenInterest_daily=OpenInterest_daily.pivot(index='time',columns='position_direction',values='open_notional').reset_index()

