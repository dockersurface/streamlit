import akshare as ak
import pandas as pd

# 获取上证指数的历史数据，判断大盘的均线情况
index_data = ak.stock_zh_index_daily(symbol="sh000001")  # 上证指数
index_data["MA5"] = index_data["close"].rolling(window=5).mean()
index_data["MA10"] = index_data["close"].rolling(window=10).mean()
index_data["MA20"] = index_data["close"].rolling(window=20).mean()
index_data["MA30"] = index_data["close"].rolling(window=30).mean()
latest_index_data = index_data.tail(1)  # 取最新一条数据

# 判断大盘当前价格与均线的位置
index_price = latest_index_data["close"].values[0]
index_ma5 = latest_index_data["MA5"].values[0]
index_ma10 = latest_index_data["MA10"].values[0]
index_ma20 = latest_index_data["MA20"].values[0]
index_ma30 = latest_index_data["MA30"].values[0]
print(index_price, index_ma5, index_ma10, index_ma20, index_ma30)

# 获取沪深A股股票列表
# 定义不同板块的代码前缀
main_board_prefix = ('60', '000')  # 上海主板和深圳主板
chuangye_board_prefix = ('300',)   # 创业板
kechuang_board_prefix = ('68',)    # 科创板
zxb_board_prefix = ('002',)        # 中小板

# 根据代码前缀筛选主板和创业板股票
def filter_main_and_chuangye(df):
    df = df[
      df['代码'].str.startswith(main_board_prefix 
      + chuangye_board_prefix 
      # + kechuang_board_prefix 
      # + zxb_board_prefix
      )
    ]
    return df

stock_zh_a_spot_df = ak.stock_zh_a_spot_em()
stock_list = filter_main_and_chuangye(stock_zh_a_spot_df)

selected_stocks_ma5 = []
selected_stocks_ma10 = []
selected_stocks_ma20 = []
selected_stocks_ma30 = []

index = 0
print(len(stock_list))
# 判断大盘的均线位置，并选择个股符合条件
for code in stock_list['代码']:
    try:
        # 获取个股的日线数据
        stock_data = ak.stock_zh_a_hist(symbol=code, period="daily", adjust="qfq", start_date="20240915", end_date="20241113")
        index +=1
        print(index, code)
        stock_data["MA5"] = stock_data["收盘"].rolling(window=5).mean()
        stock_data["MA10"] = stock_data["收盘"].rolling(window=10).mean()
        stock_data["MA20"] = stock_data["收盘"].rolling(window=20).mean()
        stock_data["MA30"] = stock_data["收盘"].rolling(window=30).mean()
        latest_stock_data = stock_data.tail(1)

        stock_price = latest_stock_data["收盘"].values[0]
        stock_ma5 = latest_stock_data["MA5"].values[0]
        stock_ma10 = latest_stock_data["MA10"].values[0]
        stock_ma20 = latest_stock_data["MA20"].values[0]
        stock_ma30 = latest_stock_data["MA30"].values[0]
        print(stock_price, stock_ma5, stock_ma10, stock_ma20, stock_ma30)
        
        # 根据大盘位置筛选个股
        if index_price > index_ma5:
            # 大盘大于MA5，筛选个股小于MA5
            if stock_price < stock_ma30:
                selected_stocks_ma30.append(code)
            elif stock_price < stock_ma20:
                selected_stocks_ma20.append(code)
            elif stock_price < stock_ma10:
                selected_stocks_ma10.append(code)
            elif stock_price < stock_ma5:
                selected_stocks_ma5.append(code)
        elif index_ma10 <= index_price <= index_ma5:
            # 大盘在MA5和MA10之间，筛选个股小于MA10
            if stock_price < stock_ma30:
                selected_stocks_ma30.append(code)
            elif stock_price < stock_ma20:
                selected_stocks_ma20.append(code)
            elif stock_price < stock_ma10:
                selected_stocks_ma10.append(code)
        elif index_ma20 < index_price <= index_ma10:
            # 大盘在MA10和MA20之间，筛选个股小于MA20
            if stock_price < stock_ma30:
                selected_stocks_ma30.append(code)
            elif stock_price < stock_ma20:
                selected_stocks_ma20.append(code)
        elif index_ma30 < index_price <= index_ma20:
            # 大盘在MA20和MA30之间，筛选个股小于MA30
            if stock_price < stock_ma30:
                selected_stocks_ma30.append(code)
        

    except Exception as e:
        # 捕获数据获取过程中的异常
        print(f"Error for stock {code}: {e}")

# 输出符合条件的股票代码
print("符合条件的股票代码30：", selected_stocks_ma30)
print("符合条件的股票代码20：", selected_stocks_ma20)
print("符合条件的股票代码10：", selected_stocks_ma10)
print("符合条件的股票代码5：", selected_stocks_ma5)

