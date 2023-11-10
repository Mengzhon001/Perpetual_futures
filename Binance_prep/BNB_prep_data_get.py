import pandas as pd
import requests
import json
################################### get the list of excganges
url = "https://api.coinalyze.net/v1/exchanges"


headers = {

    "Accept": "application/json",
    'api_key':'62dcd7fc-85a0-4209-b654-8509a1509a06'
}

response = requests.get(url, headers=headers)

data=response.text
data_dict=json.loads(data)

exchanges_list=pd.DataFrame.from_dict(data_dict)

################################### get the list of futures
url = "https://api.coinalyze.net/v1/future-markets"


headers = {

    "Accept": "application/json",
    'api_key':'62dcd7fc-85a0-4209-b654-8509a1509a06'
}

response = requests.get(url, headers=headers)

data=response.text
data_dict=json.loads(data)

prep_list=pd.DataFrame.from_dict(data_dict)
prep_list.to_csv('prep_list.csv')

############################### get the history of open interest

url = "https://api.coinalyze.net/v1/open-interest-history"
headers = {

    "Accept": "application/json",
    'api_key':'62dcd7fc-85a0-4209-b654-8509a1509a06'
}

parameters = {
    'symbols':'BTCUSDT_PERP.A',
    'interval':'daily',
    'from':1279324800,
    'to':1696377599,
    'convert_to_usd':'true'

}

response = requests.get(url, headers=headers,params=parameters)

data=response.text
data_dict=json.loads(data)

BNB_prep_openInterest=pd.DataFrame.from_dict(data_dict[0]['history'])

BNB_prep_openInterest.rename(columns = {'t':'time','c':'OpenInterest_long'}, inplace = True)
BNB_prep_openInterest['OpenInterest_short']=BNB_prep_openInterest['OpenInterest_long']

BNB_prep_openInterest['time'] = pd.to_datetime(BNB_prep_openInterest['time'],unit='s')
BNB_prep_openInterest['time']=BNB_prep_openInterest['time'].astype('string').str.split(pat=' ', expand=True)[0]

BNB_prep_openInterest.drop(['o','h','l'],axis=1,inplace=True)

############################### get the history of liquidation

url = "https://api.coinalyze.net/v1/liquidation-history"
headers = {

    "Accept": "application/json",
    'api_key':'62dcd7fc-85a0-4209-b654-8509a1509a06'
}

parameters = {
    'symbols':'BTCUSDT_PERP.A',
    'interval':'daily',
    'from':1279324800,
    'to':1696377599,
    'convert_to_usd':'true'
}

response = requests.get(url, headers=headers,params=parameters)

data=response.text
data_dict=json.loads(data)

BNB_prep_liquidation=pd.DataFrame.from_dict(data_dict[0]['history'])

############################### get the history of OHLCV

url = "https://api.coinalyze.net/v1/ohlcv-history"
headers = {

    "Accept": "application/json",
    'api_key':'62dcd7fc-85a0-4209-b654-8509a1509a06'
}

parameters = {
    'symbols':'BTCUSDT_PERP.A',
    'interval':'daily',
    'from':1279324800,
    'to':1696377599,
}

response = requests.get(url, headers=headers,params=parameters)

data=response.text
data_dict=json.loads(data)

BNB_prep_OHLCV=pd.DataFrame.from_dict(data_dict[0]['history'])

############################### data cleaning and combining
BNB_prep_OHLCV.rename(columns = {'t':'time','o':'open','h':'high','l':'low','c':'close','v':'TradingVolume_usd'}, inplace = True)
BNB_prep_OHLCV.drop(['bv','tx','btx'],axis=1,inplace=True)
BNB_prep_OHLCV['time'] = pd.to_datetime(BNB_prep_OHLCV['time'],unit='s')
BNB_prep_OHLCV['time']=BNB_prep_OHLCV['time'].astype('string').str.split(pat=' ', expand=True)[0]





BNB_prep_liquidation.rename(columns = {'t':'time','l':'liquidate_long','s':'liquidate_short'}, inplace = True)
BNB_prep_liquidation['time'] = pd.to_datetime(BNB_prep_liquidation['time'],unit='s')
BNB_prep_liquidation['time']=BNB_prep_liquidation['time'].astype('string').str.split(pat=' ', expand=True)[0]

# merge
BNB_finalData = pd.merge(BNB_prep_openInterest, BNB_prep_liquidation,how="left", on="time")
BNB_finalData = pd.merge(BNB_finalData, BNB_prep_OHLCV,how="left", on="time")

BNB_finalData=BNB_finalData[(BNB_finalData['time']>='2020-08-05')&(BNB_finalData['time']<='2023-09-26')]

BNB_finalData.to_csv('/Users/andyma/Desktop/Python /Perpetual_futures/Binance_prep/BNB_finalData.csv')
