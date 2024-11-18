import akshare as ak
import pandas as pd

# 获取A股所有上市公司财报数据
# 先获取三季报（2023年）
stock_2023_q3_df = ak.stock_yjbb_em(date = "20230930")

# 转换净利润字段为数值类型
stock_2023_q3_df['净利润'] = pd.to_numeric(stock_2023_q3_df['净利润-净利润'], errors='coerce')

# 筛选净利润在 0 到 500 万之间的公司
filtered_q3_df = stock_2023_q3_df[(stock_2023_q3_df['净利润'] > 0) & (stock_2023_q3_df['净利润'] <= 5000000)]


# 获取中报（2023年半年报）数据
stock_2023_h1_df = ak.stock_yjbb_em(date = "20240630")

# 筛选出中报营收和净利润环比增长的公司
# 环比增长是指与上一期相比的增长，因此我们需要根据财报中相关字段进行计算
stock_2023_h1_df['营收环比'] = pd.to_numeric(stock_2023_h1_df['营业收入-季度环比增长'], errors='coerce')
stock_2023_h1_df['净利润环比'] = pd.to_numeric(stock_2023_h1_df['净利润-季度环比增长'], errors='coerce')
stock_2023_h1_df['净利润-净利润'] = pd.to_numeric(stock_2023_h1_df['净利润-净利润'], errors='coerce')


# 筛选出营收和净利润环比都为正数的公司
filtered_h1_df = stock_2023_h1_df[(stock_2023_h1_df['营收环比'] > 0) & (stock_2023_h1_df['净利润环比'] > 0) & (stock_2023_h1_df['净利润-净利润'] > 0)]



# 合并三季报和中报筛选结果，找出符合条件的公司
final_df = pd.merge(filtered_q3_df, filtered_h1_df, on='股票代码', how='inner')

# 显示最终筛选的结果
print(final_df[['股票代码', '股票简称_x']])
