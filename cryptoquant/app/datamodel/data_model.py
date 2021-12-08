"""
web:  studyquant.com
author: Rudy
wechat:82789754
"""
from dataclasses import dataclass
from enum import Enum
from cryptoquant.trader.constant import (
    Direction,
    Exchange,
    OrderType,
    Product,
    Status,
    Interval
)
from cryptoquant.trader.object import (
    # TickData,
    OrderData,
    TradeData,
    AccountData,
    ContractData,
    BarData,
    OrderRequest,
    CancelRequest,
    SubscribeRequest,
    HistoryRequest,
    PositionData
)

from datetime import datetime


# Example
# class Data:
#     def get_tickdata(self,data):
#         return TickData
# {'Info': {'amount': 1909475046.793364,
#           'open': 0.113802, 'close': 0.127855,
#           'high': 0.128826, 'id': 210640693782,
#           'count': 606199, 'low': 0.111127, 'version': 210640693782,
#           'ask': [0.127857, 1705.25], 'vol': 227421510.3137062, 'bid': [0.127853, 265.77]},
#  'High': 0.128826, 'Low': 0.111127, 'Sell': 0.127857,
#  'Buy': 0.127853, 'Last': 0.127855, 'Volume': 1909475046.793364, 'Time': 1619525061394}


@dataclass
class Trade():
    Id: int
    Time: int
    Price: float = 0
    Amount: float = 0
    Type: int = 0

@dataclass
class Ticker():
    """
    Tick data contains information about:
        * last trade in market
        * orderbook snapshot
        * intraday market statistics.
    """
    symbol: str
    exchange: Exchange
    datetime: datetime
    Info: dict
    Time: int
    High: float = 0
    Low: float = 0
    Sell: float = 0
    Buy: float = 0
    Last: float = 0
    Volume: float = 0

@dataclass
class Record():
    Time: int
    Open: float = 0
    High: float = 0
    Low: float = 0
    Close: float = 0
    Volume: float = 0

@dataclass
class Order():
    Info: dict
    Id: int
    Status: int
    Type: int
    Offset: int
    Price: float = 0
    Amount: float = 0
    DealAmount: float = 0
    AvgPrice: float = 0
    ContractType: str = ''

@dataclass
class MarketOrder():
    Price: float = 0
    Amount: float = 0

@dataclass
class Depth():
    Asks:list
    Bids:list
    Time:int = 0

@dataclass
class Account():
    """
    在USDT本位，数据会有点异常
    BALANCE 代表目前可用的USDT余额
    FrozenBalance： 冻结的余额
    Stocks：一般写ETH 数量， 如果没有，USDT本位持有也是USDT, 这里只能写 USDT持仓量
    这里的STOCKS 显示的是 绑定SYMBOL的 持仓
    FrozenStocks 冻结的USDT
    """
    Info: dict
    Balance: float = 0   # quotoasset USDT 现货- 余额，      期货： 保证金余额
    FrozenBalance: float = 0     # 期货： 目前占用的保证金
    Stocks: float = 0
    FrozenStocks: float = 0
    TotalUnPnl  : float = 0  # 总账户未实现盈亏
    UsdtPos: float = 0
    # Available_stocks :float=Stocks-FrozenStocks
    # UsdtPos: float = FrozenUsdt

    def __post_init__(self):
        """"""
        self.Available_balance = self.Balance - self.FrozenBalance
        self.Available_stocks = self.Stocks - self.FrozenStocks

@dataclass
class Position():
    Info: dict
    Type: int
    MarginLevel: int
    Margin: float
    Amount: float = 0
    FrozenAmount: float = 0
    Price: float = 0
    Profit: float = 0
    ContractType: str='quarter'


class Order_Type(Enum):
    """
    Direction of order/trade/position.
    """
    ORDER_STATE_PENDING = 0
    ORDER_STATE_CLOSED = 1
    ORDER_STATE_CANCELED = 2
    ORDER_STATE_UNKNOWN = 3
    ORDER_STATE_PARTIALLY_FILLED = 4

class Order_Direction(Enum):
    """
    Direction of order/trade/position.
    """
    ORDER_TYPE_BUY = 0
    ORDER_TYPE_SELL = 1




