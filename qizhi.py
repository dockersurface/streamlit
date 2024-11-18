import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt

# 定义指数和期指代码
index_codes = ["sh000016", "sh000300", "sh000905", "sh000852"]  # 现指
futures_codes = {
    "IM": ["IM2411", "IM2412", "IM2503"],
    "IC": ["IC2411", "IC2412", "IC2503"],
    "IF": ["IF2411", "IF2412", "IF2503"],
    "IH": ["IH2411", "IH2412", "IH2503"]
}

# 获取现指数据
index_data = {}
for code in index_codes:
    index_df = ak.stock_zh_index_daily(symbol=code)
    index_data[code] = index_df['close']

# 获取期指数据
futures_data = {}
for future_type, future_codes in futures_codes.items():
    futures_data[future_type] = {}
    for code in future_codes:
        future_df = ak.futures_zh_minute_sina(symbol=code, period='1')
        futures_data[future_type][code] = future_df['close']

# 绘制折线图
plt.figure(figsize=(14, 8))

print(index_data, futures_data)
# 画现指数据
for code, data in index_data.items():
    plt.plot(data.index, data, label=f"现指 {code}")

# 画期指数据
for future_type, future_series in futures_data.items():
    for code, data in future_series.items():
        plt.plot(data.index, data, linestyle='--', label=f"{future_type} {code}")

plt.xlabel("日期")
plt.ylabel("价格")
plt.title("现指与期指对比 - 升贴水分析")
plt.legend()
plt.show()
