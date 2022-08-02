
# coding: utf-8

# In[ ]:


#%%
from datetime import datetime
from cryptoquant.app.cta_backtester.engine import BacktestingEngine, OptimizationSetting
# from cryptoquant.app.cta_strategy.studyquant_backtesting import BacktestingEngine, OptimizationSetting
from cryptoquant.app.cta_strategy.strategies.atr_rsi_strategy import (
    AtrRsiStrategy,
)




#%%
engine = BacktestingEngine()

engine.set_parameters(
    vt_symbol="IF9999.CFFEX",
    interval="1m",
    start=datetime(2020, 1, 1),
    end=datetime(2020, 4, 30),
    rate=0.3/10000,
    slippage=0.5,
    size=300,
    pricetick=0.2,
    capital=1_000_0,
)

setting = {}

engine.add_strategy(AtrRsiStrategy,setting)

# 导入数据
engine.load_data()

# 开始回测
engine.run_backtesting()
#计算收益
df = engine.calculate_result()

# 开始统计
engine.calculate_statistics()

# 开始画图
engine.show_chart()






# In[ ]:
# setting = OptimizationSetting()
# setting.set_target("sharpe_ratio")
# setting.add_parameter("atr_length", 3, 39, 1)
# setting.add_parameter("atr_ma_length", 10, 30, 1)
# engine.run_ga_optimization(setting)
#
