# https://github.com/mapicccy/funcat/blob/master/README.md
# https://mp.weixin.qq.com/s?__biz=MzI5NDAzNzExNw==&mid=2247485910&idx=1&sn=b578f0722e0cf23df08c39ce22535d84&chksm=ec69bac4db1e33d21a4476495780ec0b430c63b838caf4d79da030932038a5b20f760a24f65a&token=148233563&lang=zh_CN#rd

import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt
from ta.trend import SMAIndicator, MACD

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# 获取贵州茅台的股票数据
stock_code = "600519"
start_date = "20240101"
end_date = "20241018"

df = ak.stock_zh_a_hist(symbol=stock_code, start_date=start_date, end_date=end_date, adjust="qfq")
df['日期'] = pd.to_datetime(df['日期'])
df.set_index('日期', inplace=True)

# 计算指标
df['SMA50'] = SMAIndicator(close=df['收盘'], window=50).sma_indicator()
macd = MACD(close=df['收盘'])
df['MACD'] = macd.macd()
df['MACD_Signal'] = macd.macd_signal()

# 生成交易信号
df['Signal'] = 0
df.loc[(df['MACD'] > df['MACD_Signal']) & (df['收盘'] > df['SMA50']), 'Signal'] = 1
df.loc[(df['MACD'] < df['MACD_Signal']) & (df['收盘'] < df['SMA50']), 'Signal'] = -1

# 绘制图表
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

ax1.plot(df.index, df['收盘'], label='收盘价')
ax1.plot(df.index, df['SMA50'], label='50日均线')
ax1.set_title('贵州茅台 - 价格和50日均线')
ax1.legend()

ax2.plot(df.index, df['MACD'], label='MACD')
ax2.plot(df.index, df['MACD_Signal'], label='MACD信号线')
ax2.bar(df.index, df['MACD'] - df['MACD_Signal'], label='MACD柱状图')
ax2.set_title('MACD')
ax2.legend()

plt.tight_layout()
plt.show()

# 打印信号变化点
print(df[df['Signal'] != df['Signal'].shift(1)])