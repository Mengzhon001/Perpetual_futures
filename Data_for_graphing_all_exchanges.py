import pandas as pd
import scipy.stats as stats


##################################### process the data of Binance and initiate the final df
Data_binance = pd.read_csv('/Users/andyma/Desktop/Python /Perpetual_futures/Binance_prep/BNB_finalData.csv', index_col=0)
Data_binance.fillna(0, inplace=True)
Data_binance = Data_binance.loc[Data_binance['time']<='2023-09-26',:]
Data_binance.set_index(['time'],inplace=True)


Data_binance.index = pd.to_datetime(Data_binance.index)

# initiate the df for the final dataset to graph
GraphData_oclh_weekly = pd.DataFrame()
# add weekly data for BTC
GraphData_oclh_weekly['open'] = Data_binance.open.resample('W').first()
GraphData_oclh_weekly['close'] = Data_binance.close.resample('W').last()
GraphData_oclh_weekly['low'] = Data_binance.low.resample('W').min()
GraphData_oclh_weekly['high'] = Data_binance.high.resample('W').max()

# add weekly data for Binance
GraphData_oclh_weekly['TradingVolume_binance'] = Data_binance.TradingVolume_usd.resample('W').sum()

GraphData_oclh_weekly['liquidate_long_binance'] = Data_binance.liquidate_long.resample('W').sum()
GraphData_oclh_weekly['liquidate_short_binance'] = Data_binance.liquidate_short.resample('W').sum()
GraphData_oclh_weekly['OpenInterest_long_binance'] = Data_binance.OpenInterest_long.resample('W').last()
GraphData_oclh_weekly['OpenInterest_short_binance'] = Data_binance.OpenInterest_short.resample('W').last()


##################################### process data of Bybit

Data_bybit = pd.read_csv('/Users/andyma/Desktop/Python /Perpetual_futures/Bybit/Bybit_finalData.csv', index_col=0)
Data_bybit.fillna(0, inplace=True)
Data_bybit = Data_bybit.loc[Data_bybit['time']<='2023-09-26',:]
Data_bybit.set_index(['time'],inplace=True)

Data_bybit.index = pd.to_datetime(Data_bybit.index)

# add weekly data for Bybit
GraphData_oclh_weekly['TradingVolume_bybit'] = Data_bybit.TradingVolume_usd.resample('W').sum()

GraphData_oclh_weekly['liquidate_long_bybit'] = Data_bybit.liquidate_long.resample('W').sum()
GraphData_oclh_weekly['liquidate_short_bybit'] = Data_bybit.liquidate_short.resample('W').sum()
GraphData_oclh_weekly['OpenInterest_long_bybit'] = Data_bybit.OpenInterest_long.resample('W').last()
GraphData_oclh_weekly['OpenInterest_short_bybit'] = Data_bybit.OpenInterest_short.resample('W').last()


##################################### process data of GMX

Data_GMX = pd.read_csv('BTC_liquidation.csv', index_col=0)
Data_GMX.fillna(0, inplace=True)


Data_GMX.index = pd.to_datetime(Data_GMX.index)

# add weekly data for GMX
GraphData_oclh_weekly['TradingVolume_GMX'] = Data_GMX.TradingVolume_usd.resample('W').sum()

GraphData_oclh_weekly['liquidate_long_GMX'] = Data_GMX.liquidate_long.resample('W').sum()
GraphData_oclh_weekly['liquidate_short_GMX'] = Data_GMX.liquidate_short.resample('W').sum()
GraphData_oclh_weekly['OpenInterest_long_GMX'] = Data_GMX.OpenInterest_long.resample('W').last()
GraphData_oclh_weekly['OpenInterest_short_GMX'] = Data_GMX.OpenInterest_short.resample('W').last()

##################################### process data of Perpetual Protocol

Data_perp = pd.read_csv('/Users/andyma/Desktop/Python /Perpetual_futures/PrepProtocal/PrepProtocal_finalData.csv', index_col=0)
Data_perp.fillna(0, inplace=True)
Data_perp.set_index(['time'],inplace=True)

Data_perp.index = pd.to_datetime(Data_perp.index)

# add weekly data for Bybit
GraphData_oclh_weekly['TradingVolume_perp'] = Data_perp.TradingVolume_usd.resample('W').sum()

GraphData_oclh_weekly['liquidate_long_perp'] = Data_perp.liquidate_long.resample('W').sum()
GraphData_oclh_weekly['liquidate_short_perp'] = Data_perp.liquidate_short.resample('W').sum()
GraphData_oclh_weekly['OpenInterest_long_perp'] = Data_perp.OpenInterest_long.resample('W').last()
GraphData_oclh_weekly['OpenInterest_short_perp'] = Data_perp.OpenInterest_short.resample('W').last()

##################################### process data of GNS

Data_GNS = pd.read_csv('/Users/andyma/Desktop/Python /Perpetual_futures/GNS/GNS_polygon_liquidation.csv', index_col=0)
Data_GNS.fillna(0, inplace=True)
Data_GNS.set_index(['time'],inplace=True)

Data_GNS.index = pd.to_datetime(Data_GNS.index)

# add weekly data for Bybit
GraphData_oclh_weekly['TradingVolume_GNS'] = Data_GNS.TradingVolume_usd.resample('W').sum()

GraphData_oclh_weekly['liquidate_long_GNS'] = Data_GNS.liquidate_long.resample('W').sum()
GraphData_oclh_weekly['liquidate_short_GNS'] = Data_GNS.liquidate_short.resample('W').sum()
GraphData_oclh_weekly['OpenInterest_long_GNS'] = Data_GNS.OpenInterest_long.resample('W').last()
GraphData_oclh_weekly['OpenInterest_short_GNS'] = Data_GNS.OpenInterest_short.resample('W').last()

##################################### output the data
GraphData_oclh_weekly.fillna(0, inplace=True)
GraphData_oclh_weekly.to_csv('GraphData_oclh_weekly.csv')


#################################### descriptive statistics
stat_binance_mean=Data_binance.mean()
stat_bybit_mean=Data_bybit.mean()
stat_GMX_mean=Data_GMX.mean()
stat_GNS_mean=Data_GNS.mean()
stat_perp_mean=Data_perp.mean()

stat_binance_std=Data_binance.std()
stat_bybit_std=Data_bybit.std()
stat_GMX_std=Data_GMX.std()
stat_GNS_std=Data_GNS.std()
stat_perp_std=Data_perp.std()

#################################### SI and LIQ
SI=pd.DataFrame()
SI['SI_binance']=(Data_binance['TradingVolume_usd']*1000)/Data_binance['OpenInterest_long']
SI['SI_bybit']=(Data_bybit['TradingVolume_usd']*1000)/Data_bybit['OpenInterest_long']
SI['SI_GMX']=(Data_GMX['TradingVolume_usd'])/((Data_GMX['OpenInterest_long']+Data_GMX['OpenInterest_long'])/2)
SI['SI_GNS']=(Data_GNS['TradingVolume_usd'])/((Data_GNS['OpenInterest_long']+Data_GNS['OpenInterest_long'])/2)
SI['SI_perp']=(Data_perp['TradingVolume_usd'])/((Data_perp['OpenInterest_long']+Data_perp['OpenInterest_long'])/2)

LIQ_long=pd.DataFrame()
LIQ_long['LIQ_long_binance']=Data_binance['liquidate_long']/Data_binance['OpenInterest_long']
LIQ_long['LIQ_long_bybit']=Data_bybit['liquidate_long']/Data_bybit['OpenInterest_long']
LIQ_long['LIQ_long_GMX']=Data_GMX['liquidate_long']/Data_GMX['OpenInterest_long']
LIQ_long['LIQ_long_GNS']=Data_GNS['liquidate_long']/Data_GNS['OpenInterest_long']
LIQ_long['LIQ_long_perp']=Data_perp['liquidate_long']/Data_perp['OpenInterest_long']

LIQ_short=pd.DataFrame()
LIQ_short['LIQ_short_binance']=Data_binance['liquidate_short']/Data_binance['OpenInterest_short']
LIQ_short['LIQ_short_bybit']=Data_bybit['liquidate_short']/Data_bybit['OpenInterest_short']
LIQ_short['LIQ_short_GMX']=Data_GMX['liquidate_short']/Data_GMX['OpenInterest_short']
LIQ_short['LIQ_short_GNS']=Data_GNS['liquidate_short']/Data_GNS['OpenInterest_short']
LIQ_short['LIQ_short_perp']=Data_perp['liquidate_short']/Data_perp['OpenInterest_short']

SI_std=SI.std()
LIQ_short_std=LIQ_short.std()
LIQ_long_std=LIQ_long.std()

SI_mean=SI.mean()
LIQ_short_mean=LIQ_short.mean()
LIQ_long_mean=LIQ_long.mean()

SI.to_csv('SI_measures.csv')
LIQ_long.to_csv('LIQ_long.csv')
LIQ_short.to_csv('LIQ_short.csv')

print(stats.ttest_ind(a=LIQ_short['LIQ_short_GMX'].dropna(), b=LIQ_long['LIQ_long_GMX'].dropna(), equal_var=False))
print(stats.ttest_ind(a=LIQ_short['LIQ_short_GNS'].dropna(), b=LIQ_long['LIQ_long_GNS'].dropna(), equal_var=False))
print(stats.ttest_ind(a=LIQ_short['LIQ_short_perp'].dropna(), b=LIQ_long['LIQ_long_perp'].dropna(), equal_var=False))
print(stats.ttest_ind(a=LIQ_short['LIQ_short_binance'].dropna(), b=LIQ_long['LIQ_long_binance'].dropna(), equal_var=False))
print(stats.ttest_ind(a=LIQ_short['LIQ_short_bybit'].dropna(), b=LIQ_long['LIQ_long_bybit'].dropna(), equal_var=False))

print(stats.ttest_ind(a=Data_GMX['leverage_long'].dropna(), b=Data_GMX['leverage_short'].dropna(), equal_var=False))
print(stats.ttest_ind(a=Data_GNS['leverage_long'].dropna(), b=Data_GNS['leverage_short'].dropna(), equal_var=False))