import pandas as pd
import requests
import json


############################### get the history of open interest

url = "https://api.coinalyze.net/v1/open-interest-history"
headers = {

    "Accept": "application/json",
    'api_key':'62dcd7fc-85a0-4209-b654-8509a1509a06'
}

parameters = {
    'symbols':'BTCUSDT.6',
    'interval':'daily',
    'from':1279324800,
    'to':1696377599,
    'convert_to_usd':'true'

}

response = requests.get(url, headers=headers,params=parameters)

data=response.text
data_dict=json.loads(data)

Bybit_prep_openInterest=pd.DataFrame.from_dict(data_dict[0]['history'])

Bybit_prep_openInterest.rename(columns = {'t':'time','c':'OpenInterest_long'}, inplace = True)
Bybit_prep_openInterest['OpenInterest_short']=Bybit_prep_openInterest['OpenInterest_long']

Bybit_prep_openInterest['time'] = pd.to_datetime(Bybit_prep_openInterest['time'],unit='s')
Bybit_prep_openInterest['time']=Bybit_prep_openInterest['time'].astype('string').str.split(pat=' ', expand=True)[0]

Bybit_prep_openInterest.drop(['o','h','l'],axis=1,inplace=True)

############################### get the history of liquidation

url = "https://api.coinalyze.net/v1/liquidation-history"
headers = {

    "Accept": "application/json",
    'api_key':'62dcd7fc-85a0-4209-b654-8509a1509a06'
}

parameters = {
    'symbols':'BTCUSDT.6',
    'interval':'daily',
    'from':1279324800,
    'to':1696377599,
    'convert_to_usd':'true'
}

response = requests.get(url, headers=headers,params=parameters)

data=response.text
data_dict=json.loads(data)

Bybit_prep_liquidation=pd.DataFrame.from_dict(data_dict[0]['history'])

############################### get the history of OHLCV

url = "https://api.coinalyze.net/v1/ohlcv-history"
headers = {

    "Accept": "application/json",
    'api_key':'62dcd7fc-85a0-4209-b654-8509a1509a06'
}

parameters = {
    'symbols':'BTCUSDT.6',
    'interval':'daily',
    'from':1279324800,
    'to':1696377599,
}

response = requests.get(url, headers=headers,params=parameters)

data=response.text
data_dict=json.loads(data)

Bybit_prep_OHLCV=pd.DataFrame.from_dict(data_dict[0]['history'])

############################### data cleaning and combining
Bybit_prep_OHLCV.rename(columns = {'t':'time','o':'open','h':'high','l':'low','c':'close','v':'TradingVolume_usd'}, inplace = True)
Bybit_prep_OHLCV.drop(['bv','tx','btx'],axis=1,inplace=True)
Bybit_prep_OHLCV['time'] = pd.to_datetime(Bybit_prep_OHLCV['time'],unit='s')
Bybit_prep_OHLCV['time']=Bybit_prep_OHLCV['time'].astype('string').str.split(pat=' ', expand=True)[0]




Bybit_prep_liquidation.rename(columns = {'t':'time','l':'liquidate_long','s':'liquidate_short'}, inplace = True)
Bybit_prep_liquidation['time'] = pd.to_datetime(Bybit_prep_liquidation['time'],unit='s')
Bybit_prep_liquidation['time']=Bybit_prep_liquidation['time'].astype('string').str.split(pat=' ', expand=True)[0]

# merge
Bybit_finalData = pd.merge(Bybit_prep_openInterest, Bybit_prep_liquidation,how="left", on="time")
Bybit_finalData = pd.merge(Bybit_finalData, Bybit_prep_OHLCV,how="left", on="time")


Bybit_finalData=Bybit_finalData[(Bybit_finalData['time']>='2020-08-05')&(Bybit_finalData['time']<='2023-09-26')]
Bybit_finalData.fillna(0, inplace=True)


Bybit_finalData.to_csv('/Users/andyma/Desktop/Python /Perpetual_futures/Bybit/Bybit_finalData.csv')
