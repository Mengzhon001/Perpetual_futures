import pandas as pd
import requests
import json

######################## get the list of perp
url = "https://open-api.coinglass.com/public/v2/perpetual_market?symbol=BTC"

headers = {
    "accept": "application/json",
    "coinglassSecret": "0f515fbc9c404303a6a14d4e048da9c7"
}

response = requests.get(url, headers=headers)
data=response.text
data_dict=json.loads(data)

perp_list_BTC=pd.DataFrame.from_dict(data_dict['data']['BTC'])
