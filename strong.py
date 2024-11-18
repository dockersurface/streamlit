import akshare as ak
import pandas as pd

# 获取沪深A股的实时行情数据
stock_zh_a_spot_df = ak.stock_zh_a_spot_em()
# 将"code"列转换为标准股票代码格式
# stock_zh_a_spot_df.columns

# 定义不同板块的代码前缀
main_board_prefix = ('60', '000')  # 上海主板和深圳主板
chuangye_board_prefix = ('300',)   # 创业板
kechuang_board_prefix = ('68',)    # 科创板
zxb_board_prefix = ('002',)        # 中小板

# 根据代码前缀筛选主板和创业板股票
def filter_main_and_chuangye(df):
    df = df[
      df['代码'].str.startswith(main_board_prefix 
      # + chuangye_board_prefix 
      # + kechuang_board_prefix 
      # + zxb_board_prefix
      )
    ]
    return df

# 应用筛选函数
filtered_df = filter_main_and_chuangye(stock_zh_a_spot_df)

# 定义强势股票的筛选条件，涨幅和换手率
def get_strong_stock(df, pct_chg_threshold=9.9, turnover_rate_threshold=7):
    strong_stocks_df = df[(df["涨跌幅"] >= pct_chg_threshold) & (df["换手率"] > turnover_rate_threshold)]
    return strong_stocks_df

# 筛选符合条件的强势股票
strong_stocks_df = get_strong_stock(filtered_df)

# 输出筛选后的股票列表
print("强势筹码集中股列表：")
print(strong_stocks_df[["代码", "名称", "涨跌幅", "换手率", "成交额"]])
