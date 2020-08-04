
# coding: utf-8

# In[ ]:


#%%
from cryptoquant.app.backtesting.backtesting import BacktestingEngine, OptimizationSetting
from datetime import datetime
from cryptoquant.app.strategies.MaStrategy import (
    SQMA_strategy,
)

#%%
engine = BacktestingEngine()
engine.set_parameters(
    vt_symbol="IF1912.CFFEX",
    interval= "1m",
    start=datetime(2019, 1, 1),
    end=datetime(2020, 4, 30),
    rate=0.3/10000,
    slippage=0.2,
    size=300,
    pricetick=0.2,
    capital=1_000_000,
)

engine.add_strategy(SQMA_strategy, {})


# In[ ]:
#%%
engine.load_data()
engine.run_backtesting()
df = engine.calculate_result()
engine.calculate_statistics()
engine.show_chart()




# In[ ]:
# setting = OptimizationSetting()
# setting.set_target("sharpe_ratio")
# setting.add_parameter("atr_length", 3, 39, 1)
# setting.add_parameter("atr_ma_length", 10, 30, 1)
# engine.run_ga_optimization(setting)
#
