import numpy as np
import pandas as pd 
import qstock as qs
import backtrader as bt
import mplfinance as mpf
import matplotlib.pyplot as plt
#正常显示画图时出现的中文和负号
from pylab import mpl
mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False

#获取创业板数据
df=qs.get_data(code_list='cyb',start='20100101',end='20240906')
window_length =20  
# 窗口长度设为20  
# 计算过去20个交易日最低价的最小值，作为支撑线  
df['支撑线']= df['low'].rolling(window=window_length).min()
# 计算过去20个交易日最高价的最大值，作为阻力线  
df['阻力线']= df['high'].rolling(window=window_length).max() 
# 识别看涨突破（收盘价高于阻力线）  
df['看涨突破']= df['close']> df['阻力线'].shift()  
# 识别看跌突破（收盘价低于支撑线）  
df['看跌突破']= df['close']< df['支撑线'].shift()
# 为看涨和看跌突破点创建新列，并用NaN值填充  
df1=df.loc['20240101':]
df1['看涨突破点']= np.nan  
df1['看跌突破点']= np.nan 
 # 在出现看涨和看跌突破的位置，用收盘价填充新列 
df1.loc[df1['看涨突破'],'看涨突破点']= df1['close']  
df1.loc[df1['看跌突破'],'看跌突破点']= df1['close'] 
 # 为支撑线、阻力线、看涨突破点和看跌突破点创建附加图  
ap1 = mpf.make_addplot(df1['支撑线'], color='green') 
ap2 = mpf.make_addplot(df1['阻力线'], color='red')  
ap3 = mpf.make_addplot(df1['看涨突破点'], scatter=True, markersize=100, color='blue') 
ap4 = mpf.make_addplot(df1['看跌突破点'], scatter=True, markersize=100, color='orange') 
 # 创建带有附加图的K线图  
mpf.plot(df1, type='candle', style='charles',  addplot=[ap1, ap2, ap3, ap4], figsize=(10,6))