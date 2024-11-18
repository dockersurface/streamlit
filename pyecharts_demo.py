import akshare as ak
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Kline, Line, Bar, Grid


def fetch_stock_data(symbol, start_time, end_time,stock_name):
    # 利用 AKShare 获取股票的数据，这里只获取前 6 列
    stock_hfq_df = ak.stock_zh_a_hist(symbol, adjust="").iloc[:, :6]

    # 处理字段命名
    stock_hfq_df.columns = [
        'date',
        'open',
        'close',
        'high',
        'low',
        'volume',
    ]
    # 把 date 作为日期索引
    stock_hfq_df.index = pd.to_datetime(stock_hfq_df['date'])
    stock_hfq_df = stock_hfq_df[start_time:end_time]

    # 准备K线图所需的数据格式
    kline_data = stock_hfq_df[['open', 'close', 'low', 'high']].values.tolist()
    dates = stock_hfq_df.index.tolist()
    return kline_data, dates


def create_kline_chart(stock_code, kline_data, dates, stock_name):
    # 创建K线图
    kline = (
        Kline()
        .add_xaxis(dates)
        .add_yaxis("K线", kline_data)
        .set_global_opts(
            title_opts=opts.TitleOpts(title=f"{stock_name} K线图"),
            xaxis_opts=opts.AxisOpts(is_scale=True),
            yaxis_opts=opts.AxisOpts(is_scale=True),
            datazoom_opts=[opts.DataZoomOpts()],
        )
    )

    # 创建网格并添加K线图
    grid = Grid()
    grid.add(kline, grid_opts=opts.GridOpts(pos_left="10%", pos_right="10%", height="80%"))

    return grid


def main():
    # 指定股票代码
    stock_code = "600619"
    stock_name  = "海立股份"
    start_time = "2024-08-01"
    end_time = "2024-09-18"

    # 获取股票数据
    kline_data, dates = fetch_stock_data(stock_code, start_time, end_time, stock_name)

    # 创建K线图
    chart = create_kline_chart(stock_code, kline_data, dates, stock_name)

    # 生成HTML文件
    chart.render(f"{stock_code}_kline_chart.html")
    print(f"K线图已生成：{stock_code}_kline_chart.html")


if __name__ == "__main__":
    main()
