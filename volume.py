import akshare as ak
import pandas as pd

try:
    # 获取A股市场的实时行情数据
    stock_zh_a_spot_df = ak.stock_zh_a_spot()

    # 将成交额列转换为数值格式，便于计算总成交额
    stock_zh_a_spot_df['成交额'] = stock_zh_a_spot_df['成交额'].apply(pd.to_numeric, errors='coerce')

    # 计算A股市场的总成交额
    total_turnover = stock_zh_a_spot_df['成交额'].sum()

    # 输出总成交额（单位：亿元）
    total_turnover_yuan = total_turnover / 1e8  # 转换为亿元
    print(f"A股当日总成交额：{total_turnover_yuan:.2f} 亿元")

except akshare.utils.demjson.JSONDecodeError as e:
    print("获取数据失败，可能是网络问题或API更新，请稍后重试。")
    print(f"错误详情：{e}")
except Exception as e:
    print("发生了其他错误。")
    print(f"错误详情：{e}")
