import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# 生成示例数据（替换为Akshare获取的真实数据）
time_index = pd.date_range(start="2023-01-01 09:30", end="2023-01-02 15:00", freq="5T")
# 只保留开盘时间 9:30-11:30 和 13:00-15:00
time_index = time_index[(time_index.strftime('%H:%M') >= '09:30') & (time_index.strftime('%H:%M') <= '11:30') |
                        (time_index.strftime('%H:%M') >= '13:00') & (time_index.strftime('%H:%M') <= '15:00')]
data = {
    "上证50": np.cumsum(np.random.randn(100)),
    "沪深300": np.cumsum(np.random.randn(100)),
    "中证500": np.cumsum(np.random.randn(100)),
    "中证1000": np.cumsum(np.random.randn(100)),
}

# 创建四个子图展示各指数
fig = make_subplots(rows=2, cols=2, subplot_titles=["上证50", "沪深300", "中证500", "中证1000"])

print(time_index)
print(data)
# 模拟三个合约期差数据并设置涨跌标记
for i, index_name in enumerate(data.keys()):
    row, col = (i // 2) + 1, (i % 2) + 1
    index_data = data[index_name]
    
    for contract in range(1, 4):
        y = index_data + np.random.uniform(-0.5, 0.5, size=100)
        fig.add_trace(
            go.Scatter(
                x=time_index,
                y=y,
                mode='lines',
                name=f"{index_name} 合约{contract}",
                line=dict(width=1)
            ),
            row=row, col=col
        )

        # 基准线
        fig.add_trace(
            go.Scatter(
                x=time_index,
                y=[0] * 100,
                mode='lines',
                line=dict(color='black', dash='dash'),
                showlegend=False
            ),
            row=row, col=col
        )

        # # 颜色填充
        # fig.add_trace(
        #     go.Scatter(
        #         x=np.concatenate([time_index, time_index[::-1]]),
        #         y=np.concatenate([y, [0]*100]),
        #         fill='toself',
        #         fillcolor='rgba(255, 182, 193, 0.3)',  # 浅红色填充升水区
        #         line=dict(color='rgba(255, 182, 193, 0)'),
        #         showlegend=False
        #     ),
        #     row=row, col=col
        # )
        # fig.add_trace(
        #     go.Scatter(
        #         x=np.concatenate([time_index, time_index[::-1]]),
        #         y=np.concatenate([[0]*100, y[::-1]]),
        #         fill='toself',
        #         fillcolor='rgba(173, 216, 230, 0.3)',  # 浅蓝色填充贴水区
        #         line=dict(color='rgba(173, 216, 230, 0)'),
        #         showlegend=False
        #     ),
        #     row=row, col=col
        # )

    # 模拟条件添加涨跌标记点
    for j in range(1, 100):
        # 判断当前时刻的涨跌情况
        if index_data[j] > index_data[j-1]:  # 指数上涨
            if y[j] > y[j-1]:  # 升水扩大或贴水缩小
                fig.add_trace(
                    go.Scatter(
                        x=[time_index[j]],
                        y=[y[j]],
                        mode='markers',
                        marker=dict(color="green", size=8),  # 绿色标记表示真实上涨
                        name="真实上涨",
                        showlegend=(i == 0 and j == 1)  # 仅在第一个图的第一个点上显示图例
                    ),
                    row=row, col=col
                )
            else:  # 升水缩小或贴水扩大
                fig.add_trace(
                    go.Scatter(
                        x=[time_index[j]],
                        y=[y[j]],
                        mode='markers',
                        marker=dict(color="yellow", size=8),  # 黄色标记表示存疑上涨
                        name="存疑上涨",
                        showlegend=(i == 0 and j == 1)  # 仅在第一个图的第一个点上显示图例
                    ),
                    row=row, col=col
                )
        elif index_data[j] < index_data[j-1]:  # 指数下跌
            if y[j] > y[j-1]:  # 升水扩大或贴水缩小
                fig.add_trace(
                    go.Scatter(
                        x=[time_index[j]],
                        y=[y[j]],
                        mode='markers',
                        marker=dict(color="yellow", size=8),  # 黄色标记表示存疑下跌
                        name="存疑下跌",
                        showlegend=(i == 0 and j == 1)  # 仅在第一个图的第一个点上显示图例
                    ),
                    row=row, col=col
                )
            else:  # 升水缩小或贴水扩大
                fig.add_trace(
                    go.Scatter(
                        x=[time_index[j]],
                        y=[y[j]],
                        mode='markers',
                        marker=dict(color="red", size=8),  # 红色标记表示真实下跌
                        name="真实下跌",
                        showlegend=(i == 0 and j == 1)  # 仅在第一个图的第一个点上显示图例
                    ),
                    row=row, col=col
                )

# 调整布局
fig.update_layout(
    title="四个主指数分屏展示及升贴水趋势（含涨跌标记）",
    hovermode="x unified",
    height=800,
    width=1200,
    xaxis=dict(type="category"),
    xaxis2=dict(type="category"),
    xaxis3=dict(type="category"),
    xaxis4=dict(type="category"),
    template="plotly_white"
)

fig.show()
