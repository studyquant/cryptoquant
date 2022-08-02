"""
=========================================================
* Powered by StudyQuant

* author: Rudy
* wechat: studyquant88
======================================q===================
* Product Page: https://studyquant.com
* Copyright 2022 StudyQuant
* License (https://studyquant.com/)
* Coded by https://studyquant.com
=========================================================
* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
"""

__version__ = "1.4.0"
version = "public"


from cryptoquant.app.datamodel.constant import (
    SymbolType,
    Interval,
    Runmode,
    Direction,
    Offset,
    OrderType,
    OrderSTATUS,
    OrderOffset,
    Exchange,
)
from cryptoquant.app.datamodel.data_model import (
    Trade,
    Ticker,
    Record,
    Order,
    OrderRequest,
    MarketOrder,
    Depth,
    Account,
    Position,
)

# - 策略导入
# from cryptoquant.app.cta_strategy.strategies.double_ma_strategy import (
#     DoubleMaStrategy,
# )

from cryptoquant.app.cta_backtester.engine import BacktestingEngine, OptimizationSetting
from cryptoquant.config.config import binance_api_key, binance_secret_key
from cryptoquant.config.strategy_config import (
    ma_strategy_setting,
    ma_strategy_spot_setting,
)

# other third library
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import time

job_defaults = {"max_instances": 20}  # 最大任务数量
scheduler = BackgroundScheduler(timezone="MST", job_defaults=job_defaults)

from cryptoquant.api.api_gateway.exchange import get_exchange

if version == "public":
    from cryptoquant.api.api_gateway.build.apigateway_v7 import get_exchange, ApiGateway
    from cryptoquant.api.ccxt.build.ccxtgateway import CcxtGateway
else:

    from cryptoquant.api.api_gateway.pro.apigateway_v7 import get_exchange, ApiGateway
    from cryptoquant.api.ccxt.pro.ccxtgateway import CcxtGateway
