import pandas as pd
import requests
import json

############################### get the history of open interest

url = "https://api.coinalyze.net/v1/long-short-ratio-history"
headers = {

    "Accept": "application/json",
    'api_key':'62dcd7fc-85a0-4209-b654-8509a1509a06'
}

parameters = {
    'symbols':' BTCUSD_PERP.8 ',
    'interval':'daily',
    'from':1279324800,
    'to':1688601600

}

response = requests.get(url, headers=headers,params=parameters)

data=response.text
data_dict=json.loads(data)

BNB_prep_openInterest=pd.DataFrame.from_dict(data_dict[0]['history'])

############################### get the history of liquidation

url = "https://api.coinalyze.net/v1/liquidation-history"
headers = {

    "Accept": "application/json",
    'api_key':'62dcd7fc-85a0-4209-b654-8509a1509a06'
}

parameters = {
    'symbols':'BTC-USD.8',
    'interval':'daily',
    'from':1279324800,
    'to':1688601600,
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
    'symbols':'BTC-USD.8',
    'interval':'daily',
    'from':1279324800,
    'to':1688601600,
}

response = requests.get(url, headers=headers,params=parameters)

data=response.text
data_dict=json.loads(data)

BNB_prep_OHLCV=pd.DataFrame.from_dict(data_dict[0]['history'])

############################### data cleaning and combining
