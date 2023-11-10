import pandas as pd

##################################### process data of GMX

Data_GMX = pd.read_csv('BTC_liquidation.csv', index_col=0)
Data_GMX.fillna(0, inplace=True)


Data_GMX.index = pd.to_datetime(Data_GMX.index)

GraphData_oclh_weekly = pd.DataFrame()
# add weekly data for GMX
GraphData_oclh_weekly['leverage_long_GMX'] = Data_GMX.leverage_long.resample('W').mean()
GraphData_oclh_weekly['leverage_short_GMX'] = Data_GMX.leverage_short.resample('W').mean()

GraphData_oclh_weekly['less_than_1X_GMX'] = Data_GMX['Less than 1.1X'].resample('W').sum()
GraphData_oclh_weekly['1X_5X_GMX'] = Data_GMX['1.1X - 5X'].resample('W').sum()
GraphData_oclh_weekly['5X_10X_GMX'] = Data_GMX['5X - 10X'].resample('W').sum()
GraphData_oclh_weekly['10X_15X_GMX'] = Data_GMX['10X - 15X'].resample('W').sum()
GraphData_oclh_weekly['15X_20X_GMX'] = Data_GMX['15X - 20X'].resample('W').sum()
GraphData_oclh_weekly['20X_25X_GMX'] = Data_GMX['20X - 25X'].resample('W').sum()
GraphData_oclh_weekly['25X_30X_GMX'] = Data_GMX['25X - 30X'].resample('W').sum()
GraphData_oclh_weekly['30X_35X_GMX'] = Data_GMX['30X - 35X'].resample('W').sum()
GraphData_oclh_weekly['35X_40X_GMX'] = Data_GMX['35X - 40X'].resample('W').sum()
GraphData_oclh_weekly['40X_45X_GMX'] = Data_GMX['40X - 45X'].resample('W').sum()
GraphData_oclh_weekly['45X_50X_GMX'] = Data_GMX['45X - 50X'].resample('W').sum()
GraphData_oclh_weekly['more_than_50X_GMX'] = Data_GMX['More than 50X'].resample('W').sum()


##################################### process data of GNS

Data_GNS = pd.read_csv('/Users/andyma/Desktop/Python /Perpetual_futures/GNS/GNS_polygon_liquidation.csv', index_col=0)
Data_GNS.fillna(0, inplace=True)
Data_GNS.set_index(['time'],inplace=True)

Data_GNS.index = pd.to_datetime(Data_GNS.index)

# add weekly data for GNS
GraphData_oclh_weekly['leverage_long_GNS'] = Data_GNS.leverage_long.resample('W').mean()
GraphData_oclh_weekly['leverage_short_GNS'] = Data_GNS.leverage_short.resample('W').mean()

GraphData_oclh_weekly['less_than_1X_GNS'] = Data_GNS['Less than 1.1X'].resample('W').sum()
GraphData_oclh_weekly['1X_5X_GNS'] = Data_GNS['1.1X - 5X'].resample('W').sum()
GraphData_oclh_weekly['5X_10X_GNS'] = Data_GNS['5X - 10X'].resample('W').sum()
GraphData_oclh_weekly['10X_15X_GNS'] = Data_GNS['10X - 15X'].resample('W').sum()
GraphData_oclh_weekly['15X_20X_GNS'] = Data_GNS['15X - 20X'].resample('W').sum()
GraphData_oclh_weekly['20X_25X_GNS'] = Data_GNS['20X - 25X'].resample('W').sum()
GraphData_oclh_weekly['25X_30X_GNS'] = Data_GNS['25X - 30X'].resample('W').sum()
GraphData_oclh_weekly['30X_35X_GNS'] = Data_GNS['30X - 35X'].resample('W').sum()
GraphData_oclh_weekly['35X_40X_GNS'] = Data_GNS['35X - 40X'].resample('W').sum()
GraphData_oclh_weekly['40X_45X_GNS'] = Data_GNS['40X - 45X'].resample('W').sum()
GraphData_oclh_weekly['45X_50X_GNS'] = Data_GNS['45X - 50X'].resample('W').sum()
GraphData_oclh_weekly['more_than_50X_GNS'] = Data_GNS['More than 50X'].resample('W').sum()

###### output the data
GraphData_oclh_weekly.fillna(0, inplace=True)
GraphData_oclh_weekly.to_csv('GraphData_DEX.csv')
