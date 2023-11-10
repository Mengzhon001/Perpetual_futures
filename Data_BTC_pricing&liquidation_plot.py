import pandas as pd

BTC_liquidation = pd.read_csv('BTC_liquidation.csv', index_col=0)

BTC_liquidation.index = pd.to_datetime(BTC_liquidation.index)
# fill nan with 0
BTC_liquidation['liquidate-long']=BTC_liquidation['liquidate-long'].fillna(0)
BTC_liquidation['liquidate-short']=BTC_liquidation['liquidate-short'].fillna(0)
BTC_liquidation['TradingVolume_usd']=BTC_liquidation['TradingVolume_usd'].fillna(0)

# BTC_oclh=BTC_liquidation[['open','close','low','high','volume_usd']]
# BTC_oclh=BTC_oclh.set_index('time')
# BTC_oclh.index = pd.to_datetime(BTC_oclh.index)

# deriving the weekly data
BTC_oclh_weekly = pd.DataFrame()
BTC_oclh_weekly['open'] = BTC_liquidation.open.resample('W').first()
BTC_oclh_weekly['close'] = BTC_liquidation.close.resample('W').last()
BTC_oclh_weekly['low'] = BTC_liquidation.low.resample('W').min()
BTC_oclh_weekly['high'] = BTC_liquidation.high.resample('W').max()
BTC_oclh_weekly['TradingVolume_usd'] = BTC_liquidation.TradingVolume_usd.resample('W').sum()

liquidation_weekly = pd.DataFrame()
BTC_liquidation.rename(columns = {'liquidate-long':'liquidate_long','liquidate-short':'liquidate_short'}, inplace = True)
liquidation_weekly['liquidate_long'] = BTC_liquidation.liquidate_long.resample('W').sum()
liquidation_weekly['liquidate_short'] = BTC_liquidation.liquidate_short.resample('W').sum()

BTC_oclh_weekly.to_csv('BTC_oclh_weekly.csv')
liquidation_weekly.to_csv('liquidation_weekly.csv')


### plot the BTC pricing and the liquidation volume
# import mplfinance as mpf
# # 设置mplfinance的蜡烛颜色，up为阳线颜色，down为阴线颜色
# my_color = mpf.make_marketcolors(up='g',
#                                  down='r',
#                                  edge='inherit',
#                                  wick='inherit',
#                                  volume='inherit')
# # 设置图表的背景色
# my_style = mpf.make_mpf_style(marketcolors=my_color,
#                               figcolor='(0.82, 0.83, 0.85)',
#                               gridcolor='(0.82, 0.83, 0.85)')
#
# fig = mpf.figure(style=my_style, figsize=(12, 8), facecolor=(0.82, 0.83, 0.85))
# # 添加三个图表，四个数字分别代表图表左下角在figure中的坐标，以及图表的宽（0.88）、高（0.60）
# ax1 = fig.add_subplot(4, 1, 1)
# # ax1 = fig.add_axes([0.06, 0.20, 0.88, 0.20])
# # 添加第二、三张图表时，使用sharex关键字指明与ax1在x轴上对齐，且共用x轴
# ax2 = fig.add_subplot(4, 1, 2,sharex=ax1)
# # ax2 = fig.add_axes([0.06, 0.05, 0.88, 0.15], sharex=ax1)
# ax3 = fig.add_subplot(4, 1, 3,sharex=ax1)
# ax4 = fig.add_subplot(4, 1, 4,sharex=ax1)
#
# # 设置三张图表的Y轴标签
# ax1.set_ylabel('price')
# ax2.set_ylabel('GMX\nTrading volume')
# ax3.set_ylabel('GMX\nLiquidation/Trading volume')
# ax4.set_ylabel('GMX\nLiquidation')
#
#
#
#
# ap = []
# ap.append(mpf.make_addplot(liquidation_weekly['long'], type='line', color='tomato', ax=ax4, linestyle="-", linewidths=2))
# ap.append(mpf.make_addplot(liquidation_weekly['short'], type='line', color='mediumpurple', ax=ax4, linestyle="-", linewidths=2))
# ap.append(mpf.make_addplot(BTC_oclh_weekly['trading_volume'], type='bar', color='b', ax=ax2))
# ap.append(mpf.make_addplot((liquidation_weekly['total']/BTC_oclh_weekly['trading_volume']), type='line', color='tomato', ax=ax3, linestyle="-", linewidths=2))
#
# ax4.plot(pd.to_datetime(liquidation_weekly.index),liquidation_weekly['total'], label='label2')
#
# ax1.get_xaxis().set_visible(False) #清空横轴坐标
# ax2.get_xaxis().set_visible(False) #清空横轴坐标
# ax3.get_xaxis().set_visible(False) #清空横轴坐标
#
# mpf.plot(BTC_oclh_weekly,
# 		 ax=ax1,
#          addplot=ap,
# 		 type='candle',
# 		 style=my_style)
#
#
# savepath = 'GMX liquidation.png'
# fig.savefig(savepath)
# fig.show()



# ###############################################
# def style_model_light():
#     mc = mpf.make_marketcolors(up='#F8F8F8',down="#14b143", #up='black',down='#54fcfc',
#                                edge= {'up':'#ef232a','down':"#14b143"},
#                                wick={'up':'#ef232a','down':"#14b143"},
#                                volume={'up':'#ef232a','down':"#14b143"},
#                                ohlc='black')
#     mavc = [
#         '#13294B',
#         'blue',
#         '#E89B01',
#         '#BB29BB',
#         '#E96D39',
#         '#99513E',
#         '#43C5DF',
#         '#FFCD00',
#     ]
#     grid_kwargs = dict(
#                     gridcolor     = '#ef232a',
#                     gridstyle     = ':',
#                     gridaxis =     'horizontal',
#                     rc={
#                         'font.family': 'SimHei',
#                         'patch.linewidth' : 1.0,
#                         'lines.linewidth' : 1.0,
#                         'figure.titlesize' : 'x-large',
#                         'figure.titleweight' : 'semibold'
#                     },
#                        )
#
#     s = mpf.make_mpf_style(base_mpl_style='bmh',marketcolors=mc,facecolor = '#F8F8F8',y_on_right=False,mavcolors = mavc,**grid_kwargs )
#     return s
#
#
# ax_title='Liquidation GMX'
# s = style_model_light() # 使用自定义的light主题
# kwargs = dict(
#     type='candle',
#     mav=(5,20,60),
#     scale_width_adjustment = dict(volume=0.5, candle=1.15,lines=0.65),
#
#     xrotation=15,
#     ylabel='Bitcoin price',
#     ylabel_lower='GMX\nLiquidated volume',
# )
# fig = mpf.figure(style=style_model_light(),figsize=(19, 9))
# ax1 = fig.add_subplot(2, 1, 1)
# ax1.set_title(ax_title,
#               fontsize=24,
#               # backgroundcolor='white',
#               fontweight='bold',
#               color='#232323',
#               verticalalignment="top")
# ax1.spines["top"].set_visible(False)  # 上轴不显示
#
# ax2 = fig.add_subplot(4, 1, 3,sharex=ax1)
# # 添加vol均线
#
# apds = [
#     mpf.make_addplot(liquidation_weekly['long'], ax=ax2, type='line', color='r', linestyle="-", linewidths=3),#添加vol均线
#     mpf.make_addplot(liquidation_weekly['short'], ax=ax2, type='line', color='blue', linestyle="-", linewidths=3)#添加vol均线
#             ]
#
# ax1.get_xaxis().set_visible(False) #清空横轴坐标
# mpf.plot(BTC_oclh_weekly, ax=ax1, addplot=apds,**kwargs)
# savepath = 'ax作图测试.png'
# fig.savefig(savepath)
# fig.show()