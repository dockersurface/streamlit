import akshare as ak
import pandas as pd
import datetime as dt
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder


# 获取当前日期
today = dt.date.today()

 # 格式化日期为字符串
start_date_str = today.strftime('%Y-%m-%d 09:29:00')
end_date_str = today.strftime('%Y-%m-%d 15:01:00')


pd.set_option('display.width',None)
 
pd.set_option("display.max_rows", 1000)#可显示1000行
pd.set_option("display.max_columns", 1000)#可显示1000列
 
pd.set_option('display.max_rows', None)#显示全部行
pd.set_option('display.max_columns', None)#显示全部列
 
pd.options.display.max_rows = 300#显示300行
 
# 恢复默认
pd.reset_option("display.max_rows")#恢复默认设置

def filter_recent_data(df, days=1, end_date=None):
    """
    根据指定的天数范围筛选 DataFrame 中的日期数据。

    参数：
    - df: 包含数据的 DataFrame，index 应为日期
    - days: 要筛选的天数范围（默认值为1天）
    - end_date: 筛选的结束日期，默认为今天

    返回：
    - 筛选后的 DataFrame
    """
    if end_date is None:
        end_date = dt.datetime.today()
    
    # 确保 df.index 是 datetime 格式
    df.index = pd.to_datetime(df.index)
    
    start_date = end_date - dt.timedelta(days=days)
    return df[(df.index >= start_date_str) & (df.index <= end_date_str)]

# 定义现货指数和期指代码
# 映射字典
index_name_map = {
    "000016": "上证50",
    "000300": "沪深300",
    "000905": "中证500",
    "000852": "中证1000"
}
spot_indices = ["000016", "000300", "000905", "000852"]
# spot_indices = ["000016"]
futures_dict = {
    "000852": ["IM2412", "IM2501", "IM2503"],
    "000905": ["IC2412", "IC2501", "IC2503"],
    "000300": ["IF2412", "IF2501", "IF2503"],
    "000016": ["IH2412", "IH2501", "IH2503"]
}

# 获取现货指数数据
spot_data = {}
for index in spot_indices:
    data = ak.index_zh_a_hist_min_em(symbol=index, period="5", start_date=start_date_str, end_date=end_date_str)
    data.set_index("时间", inplace=True)
    spot_data[index] = data["收盘"]

# 获取期指数据
futures_data = {}
for fut, contracts in futures_dict.items():
    for contract in contracts:
        data = ak.futures_zh_minute_sina(symbol=contract, period="5")
        data.set_index("datetime", inplace=True)
        futures_data[contract] = data["close"]

# 合并数据
df_spot = pd.DataFrame(spot_data)
df_futures = pd.DataFrame(futures_data)
df_spot_recent = filter_recent_data(df_spot, days=1, end_date=None)
df_futures_recent = filter_recent_data(df_futures, days=1, end_date=None)


# 计算期差（升贴水）
spread_data = {}
for spot_index in spot_indices:
    for contract in futures_dict[spot_index]:
        # 期差 = 期货收盘价 - 现货收盘价
        spot_prices = df_spot_recent[spot_index]
        futures_prices = df_futures_recent[contract]
        spread_data[f"{contract}"] = futures_prices - spot_prices

# 筛选并整理为长表格式
long_data = []
for spot_index, contracts in futures_dict.items():
    for contract in contracts:
        if contract in spread_data:
            temp_df = pd.DataFrame({
                "时间": spread_data[contract].index,
                "合约": contract,
                "期差值": spread_data[contract].values,
                "分组": spot_index
            })
            long_data.append(temp_df)

# 合并所有长表数据
df_long = pd.concat(long_data, ignore_index=True)

# 绘制分组柱状图
for group in futures_dict.keys():
    st.subheader(f"期差表格 - {index_name_map[group]}")
    group_data = df_long[df_long["分组"] == group]
    group_data['时间'] = group_data['时间'].dt.strftime('%H:%M')
        # 将长格式数据转换为宽格式
    df_wide_group = group_data.pivot(index='时间', columns='合约', values='期差值')
    # 重置索引，使'时间'列变回数据框的一列
    df_wide_group.reset_index(inplace=True)
    # 将宽格式数据四舍五入至两位小数
    df_wide_group = df_wide_group.round(2)

    # 使用 AgGrid 优化展示
    gb = GridOptionsBuilder.from_dataframe(df_wide_group)
    # gb.configure_pagination(paginationAutoPageSize=True)  # 自动分页
    # 显示完整表头，禁用排序
    for col in df_wide_group.columns:
        gb.configure_column(
            col,
            pinned="left" if col == "时间" else None,  # 固定时间列
            headerTooltip=col,  # 确保表头显示完整
            sortable=False,      # 禁用排序
            lockPosition=True,    # 固定表头，禁止移动
            flex=1 if col != "时间" else .7  # 使用 flex 参数设置宽度比例
        )
    grid_options = gb.build()
    
    AgGrid(
        df_wide_group,
        gridOptions=grid_options,
        enable_enterprise_modules=False,
        theme="streamlit",  # 可选主题： "light", "dark", "blue", "streamlit"
        fit_columns_on_grid_load=True,
        reload_data=False,
        domLayout='autoHeight',  # 禁用垂直滚动条，使高度自动适应
    )
    # 打印该组的宽格式数据
    # print(f"组 {group} 的宽格式数据：")
    # print(df_wide_group)
    # print("\n")
    # st.table(df_wide_group)
    # print(group_data)
    # st.bar_chart(data=group_data, x="时间", y="期差值", color="合约", stack=False)
    
# df = pd.DataFrame(spread_data)
# st.line_chart(df)
