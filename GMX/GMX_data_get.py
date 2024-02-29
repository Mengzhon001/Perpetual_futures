
import json
import requests
import pandas as pd
import io

############# levergae with average volume
params = {
  "format": "csv"
}
r = requests.get('https://api.dune.com/api/v1/query/2637836/results/csv?api_key=sGepKvsNuJCeGPb1dk7buOxejEnDxzM5', params=params)
r = r.content
GMX_WBTC_leverage = pd.read_csv(io.StringIO(r.decode('utf-8')))
GMX_WBTC_leverage.to_csv('/Users/andyma/Desktop/Projects/Roger/Data/GMX_WBTC_leverage.csv')

############# levergae (with categories of levergae)
params = {
  "format": "csv"
}
r = requests.get('https://api.dune.com/api/v1/query/2644988/results/csv?api_key=sGepKvsNuJCeGPb1dk7buOxejEnDxzM5', params=params)
r = r.content
GMX_WBTC_leverage_categories = pd.read_csv(io.StringIO(r.decode('utf-8')))
GMX_WBTC_leverage_categories.to_csv('/Users/andyma/Desktop/Projects/Roger/Data/GMX_WBTC_leverage_categories.csv')


############## open interest
params = {
  "format": "csv"
}
r = requests.get('https://api.dune.com/api/v1/query/2637842/results/csv?api_key=sGepKvsNuJCeGPb1dk7buOxejEnDxzM5', params=params)
r = r.content
GMX_WBTC_OpenInterest = pd.read_csv(io.StringIO(r.decode('utf-8')))
GMX_WBTC_OpenInterest.to_csv('/Users/andyma/Desktop/Projects/Roger/Data/GMX_WBTC_open_interest.csv')

############## liquidation
params = {
  "format": "csv"
}
r = requests.get('https://api.dune.com/api/v1/query/2637376/results/csv?api_key=sGepKvsNuJCeGPb1dk7buOxejEnDxzM5', params=params)
r = r.content
GMX_WBTC_liquidation = pd.read_csv(io.StringIO(r.decode('utf-8')))
GMX_WBTC_liquidation.to_csv('/Users/andyma/Desktop/Projects/Roger/Data/GMX_WBTC_liquidation.csv')

############## trading volume daily
params = {
  "format": "csv"
}
r = requests.get('https://api.dune.com/api/v1/query/2638030/results/csv?api_key=sGepKvsNuJCeGPb1dk7buOxejEnDxzM5', params=params)
r = r.content
GMX_WBTC_TradingVolume = pd.read_csv(io.StringIO(r.decode('utf-8')))
GMX_WBTC_TradingVolume.to_csv('/Users/andyma/Desktop/Projects/Roger/Data/GMX_WBTC_tradingVolume.csv')