import streamlit as st
import plotly.graph_objects as go

# 创建数据
categories = ['A', 'B', 'C', 'D', 'E']
values1 = [10, 20, 30, 40, 50]
values2 = [15, 25, 35, 45, 55]

# 创建柱状图
fig = go.Figure()

# 添加两个柱状图系列
fig.add_trace(go.Bar(x=categories, y=values1, name='Series 1'))
fig.add_trace(go.Bar(x=categories, y=values2, name='Series 2'))

# 设置图表布局
fig.update_layout(
    title='点击图例隐藏系列',
    barmode='group',
    xaxis_title='类别',
    yaxis_title='值',
    legend_title='图例'
)

# 显示图表
st.plotly_chart(fig)
