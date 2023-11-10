import requests
import json
import pandas as pd

def TradingHistory(symbol):
    url_1='https://min-api.cryptocompare.com/data/v2/histoday?fsym='
    url_2='&tsym=USD&allData=1&api_key=0b640570752da036f31a0d7ea31a1ba6cf9ecf6a06ec5cdd1d003f554bd55caa'
    url=url_1+str(symbol)+url_2
    headers = {
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    data = response.text
    data_dict = json.loads(data)
    return data_dict
pass


# initate the dataframe on daily close price
Data_BTC=TradingHistory('BTC')
Data_BTC_OHLC=pd.DataFrame.from_dict(Data_BTC['Data']['Data'])


Data_BTC_OHLC.to_csv('BTC_OHLC_data.csv')