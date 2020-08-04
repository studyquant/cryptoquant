
# coding: utf-8

# In[ ]:


#%%
from cryptoquant.app.backtesting.backtesting import BacktestingEngine, OptimizationSetting
from datetime import datetime
from cryptoquant.app.strategies.multi_timeframe_strategy import (
    MultiTimeframeStrategy,
)

#%%
engine = BacktestingEngine()
engine.set_parameters(
    vt_symbol="XBTUSD.BITMEX",
    interval= "1m",
    start=datetime(2020, 1, 1),
    end=datetime(2020, 4, 30),
    rate=0.3/10000,
    slippage=0.5,
    size=1,
    pricetick=0.5,
    capital=1_000_0,
)

setting = {}

# 加载策略
engine.add_strategy(MultiTimeframeStrategy,setting)


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




