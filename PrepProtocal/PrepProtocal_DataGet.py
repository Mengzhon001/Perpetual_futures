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


############ open interest constructing
# Daily_last_trans = Prep_transaction.groupby(['time','trader_address'],as_index = False)['hour_min_sec'].max()
# openInterest_raw=Daily_last_trans.merge(Prep_transaction, on=['time', 'hour_min_sec','trader_address'])
# openInterest_raw=openInterest_raw.drop(['trader_address','hour_min_sec','evt_index','exchanged_position_notional','exchanged_position_size','realized_pnl','liq_tx_or_not'],axis=1)
# openInterest=openInterest_raw.groupby(['time','direction'],as_index=False)['open_notional'].sum()

#### for transactions that open or increase the positions (realized_pnl==0)
openInterest_openPosition_daily=Prep_transaction[Prep_transaction['realized_pnl']==0].groupby(['time','direction'],as_index=False)['exchanged_position_notional'].sum()

#### for transactions that reverse the positions (realized_pnl!=0)&(exchanged_position_notional*open_notional>0)
transactoions_reverse=Prep_transaction[(Prep_transaction['realized_pnl']!=0)&(Prep_transaction['exchanged_position_notional']*Prep_transaction['open_notional']>0)]
# for closed part
transactoions_reverse['closed_part']=(transactoions_reverse['exchanged_position_notional']-transactoions_reverse['open_notional']-transactoions_reverse['realized_pnl'])
openInterest_reversePosition_closedPart_daily=transactoions_reverse.groupby(['time','direction'],as_index=False)['closed_part'].sum()
# for the open part
openInterest_reversePosition_openPart_daily=transactoions_reverse.groupby(['time','direction'],as_index=False)['open_notional'].sum()

#### for transactions that close or decrease the positions (realized_pnl!=0)&(exchanged_position_notional*open_notional<=0)
openInterest_closePosition_daily=Prep_transaction[(Prep_transaction['realized_pnl']!=0)&(Prep_transaction['exchanged_position_notional']*Prep_transaction['open_notional']<=0)].groupby(['time','direction'],as_index=False)['exchanged_position_notional'].sum()

# pivoting the grouped transactions
openInterest_openPosition_daily=openInterest_openPosition_daily.pivot(index='time',columns='direction',values='exchanged_position_notional').reset_index()
openInterest_closePosition_daily=openInterest_closePosition_daily.pivot(index='time',columns='direction',values='exchanged_position_notional').reset_index()
openInterest_reversePosition_closedPart_daily=openInterest_reversePosition_closedPart_daily.pivot(index='time',columns='direction',values='closed_part').reset_index()
openInterest_reversePosition_openPart_daily=openInterest_reversePosition_openPart_daily.pivot(index='time',columns='direction',values='open_notional').reset_index()

# adjusting the lebaling of the transactions
openInterest_closePosition_daily.rename(columns = {'long':'short','short':'long'}, inplace = True)
openInterest_reversePosition_closedPart_daily.rename(columns = {'long':'short','short':'long'}, inplace = True)

# adjusting the date
date=list(openInterest_openPosition_daily['time'])
frame_date = pd.DataFrame(date, columns=['time'])
openInterest_reversePosition_closedPart_daily=pd.merge(frame_date, openInterest_reversePosition_closedPart_daily, how="left", on="time")
openInterest_reversePosition_openPart_daily=pd.merge(frame_date, openInterest_reversePosition_openPart_daily, how="left", on="time")

# fill the openPart and closedPart dataframe the nan cell with 0
openInterest_reversePosition_closedPart_daily.fillna(0,inplace=True)
openInterest_reversePosition_openPart_daily.fillna(0,inplace=True)

# sum and calculate the daily change in open interest
openInterest_change_daily=openInterest_openPosition_daily.add(openInterest_closePosition_daily)
openInterest_change_daily=openInterest_change_daily.add(openInterest_reversePosition_openPart_daily)
openInterest_change_daily=openInterest_change_daily.add(openInterest_reversePosition_closedPart_daily)

openInterest_change_daily.drop('time',axis=1)
openInterest_change_daily['time']=openInterest_openPosition_daily['time']
openInterest_change_daily.sort_values(['time'],ascending=True,inplace=True)

# cumulate the change in open position
openInterest_change_daily['OpenInterest_long']=openInterest_change_daily['long'].cumsum()
openInterest_change_daily['OpenInterest_short']=openInterest_change_daily['short'].cumsum()



openInterest = pd.DataFrame(date, columns=['time'])
openInterest['long']=openInterest_change_daily['long'].cumsum()
openInterest['long']=openInterest_change_daily['long'].cumsum()
