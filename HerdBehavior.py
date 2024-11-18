# 羊群效应（Herd Behavior）在经济学中指的是个体在决策过程中，受到他人选择影响，
# 而倾向于跟随群体行为的现象。这种现象并非总是基于理性判断，有时是出于对信息的追求，
# 有时则是为了避免与众不同所带来的不确定性和风险。在金融市场中，这种行为特征尤为突出，
# 它可以解释市场的过度反应或者波动性增强等现象。当足够多的投资者盲目跟随他人购买某种
# 股票时，其价格可能会被推高到不合理的水平。相反，当投资者恐慌性抛售时，也可能导致股
# 价迅速下跌，超出其基本面所能解释的范围。这种群体行为强化了市场的波动性，并可能诱
# 发系统性风险。

import seaborn as sns
import matplotlib.pyplot as plt

import qstock as qs
import numpy as np
import pandas as pd
#上证50成份股
codes=qs.index_member('sz50')['股票代码'].tolist()
prices=qs.get_price(code_list=codes,start='20210201',end='20240314',fqt=2)
rets=prices.dropna(axis=1).pct_change().dropna()

# 计算交叉相关性矩阵
correlation_matrix = rets.corr()

# 可视化交叉相关性矩阵
sns.heatmap(correlation_matrix, cmap='coolwarm', annot=False)
plt.title('Cross-Sectional Correlation Matrix')
plt.show()

# 分析交叉相关性
average_correlation = correlation_matrix.mean().mean()
print(f"上证50成分股2021-2024的整体交叉相关性: {average_correlation:.3f}")