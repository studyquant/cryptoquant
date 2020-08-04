from pathlib import Path

from cryptoquant.trader.app import BaseApp
from cryptoquant.trader.constant import Direction
from cryptoquant.trader.object import TickData, BarData, TradeData, OrderData
from cryptoquant.trader.utility import BarGenerator, ArrayManager


from cryptoquant.app.strategies.StrategyTemplate import CtaTemplate
from cryptoquant.app.strategies.engine import CtaEngine
from cryptoquant.app.backtesting.base import APP_NAME, StopOrder


# from .engine import CtaEngine
# from .backtesting import BacktestingEngine, OptimizationSetting
# from .template import CtaTemplate, CtaSignal, TargetPosTemplate




import numpy as np
import talib
from cryptoquant.trader.constant import (
    Direction,
    OrderType,
    Interval,
    Exchange,
    Offset,
    Status)



import traceback
from cryptoquant.trader.event import EVENT_TICK,EVENT_TRADE,EVENT_ORDER,EVENT_POSITION,EVENT_KLINE,EVENT_OPEN_ORDER,EVENT_LOG,\
EVENT_ACCOUNT,EVENT_CONTRACT
from cryptoquant.trader.ArrayManager import ArrayManager, current_minute, scheduleTime, crossover, \
    crossunder
from cryptoquant.trader.object import TickData, BarData, TradeData, OrderData
from cryptoquant.trader.utility import BarGenerator, ArrayManager



class CtaStrategyApp(BaseApp):
    """"""
    app_name = APP_NAME
    app_module = __module__
    app_path = Path(__file__).parent
    display_name = "CTA策略"
    engine_class = CtaEngine
    widget_name = "CtaManager"
    icon_name = "cta.ico"
