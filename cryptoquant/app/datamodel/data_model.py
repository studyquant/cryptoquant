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
    Interval,
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
    PositionData,
)

from datetime import datetime


@dataclass
class Trade:
    Id: int
    Time: int
    Price: float = 0
    Amount: float = 0
    Type: int = 0


@dataclass
class LeverageInfo:
    symbol: str
    leverage_level:int=1 #杠杆倍数
    marge_mode: str = "cross"
    direction:str = Direction.LONG.value


@dataclass
class Ticker:
    """
    Tick data contains information about:
        * last trade in market
        * orderbook snapshot
        * intraday market statistics.
    """

    symbol: str
    exchange: Exchange
    datetime= datetime.now()
    Info: dict
    Time: int
    High: float = 0
    Low: float = 0
    Sell: float = 0
    Buy: float = 0
    Last: float = 0
    Volume: float = 0
    limit_up = None
    limit_down = None
    def __post_init__(self):
        """"""
        self.close = self.close_price = self.Last
        self.ask_price_1 = self.Sell
        self.bid_price_1 = self.Buy


@dataclass
class Record:
    Time: int
    Open: float = 0
    High: float = 0
    Low: float = 0
    Close: float = 0
    Volume: float = 0


@dataclass
class Order:
    """
    {
    Info        : {...},         // 请求交易所接口后，交易所接口应答的原始数据，回测时无此属性
    Id          : 123456,        // 交易单唯一标识
    Price       : 1000,          // 下单价格，注意市价单的该属性可能为0或者-1
    Amount      : 10,            // 下单数量，注意市价单的该属性可能为金额并非币数
    DealAmount  : 10,            // 成交数量，如果交易所接口不提供该数据则可能使用0填充
    AvgPrice    : 1000,          // 成交均价，注意有些交易所不提供该数据。不提供、也无法计算得出的情况该属性设置为0
    Status      : 1,             // 订单状态，参考常量里的订单状态，例如：ORDER_STATE_CLOSED
    Type        : 0,             // 订单类型，参考常量里的订单类型，例如：ORDER_TYPE_BUY
    Offset      : 0              // 数字货币期货的订单数据中订单的开平仓方向。ORDER_OFFSET_OPEN为开仓方向，ORDER_OFFSET_CLOSE为平仓方向
    ContractType : ""            // 现货订单中该属性为""即空字符串，期货订单该属性为具体的合约代码
}
    """
    Info: dict
    Id: int
    Status: int
    Type: str #
    Offset: str
    Price: float = 0
    Amount: float = 0
    DealAmount: float = 0
    AvgPrice: float = 0
    ContractType: str = ""

    def __post_init__(self):
        msg = f"{self.Type}: price:{self.Price} @ {self.Amount} volume, order_id {self.Id}"

    def __repr__(self):
        """
        self.log(
            "{}: price:{} @ {} volume, order_id {}".format(
                order.direction, order.Price, order.volume, order.orderid
            )
        )
        """
        msg = f"{self.Type}: price:{self.Price} @ {self.Amount} volume, order_id {self.Id}"
        return msg


@dataclass
class MarketOrder:
    Price: float = 0
    Amount: float = 0


@dataclass
class Depth:
    Asks: list
    Bids: list
    Time: int = 0


@dataclass
class Account:
    """
    在USDT本位，数据会有点异常
    BALANCE 代表目前可用的USDT余额
    FrozenBalance： 冻结的余额
    Stocks：一般写ETH 数量， 如果没有，USDT本位持有也是USDT, 这里只能写 USDT持仓量
    这里的STOCKS 显示的是 绑定SYMBOL的 持仓
    FrozenStocks 冻结的USDT
    """

    Info: dict
    Balance: float = 0  # quotoasset USDT 现货- 余额，      期货： 保证金余额
    FrozenBalance: float = 0  # 期货： 目前占用的保证金
    Stocks: float = 0
    FrozenStocks: float = 0
    TotalUnPnl: float = 0  # 总账户未实现盈亏
    UsdtPos: float = 0
    # Available_stocks :float=Stocks-FrozenStocks
    # UsdtPos: float = FrozenUsdt

    def __post_init__(self):
        """"""
        self.Available_balance = self.Balance - self.FrozenBalance
        self.Available_stocks = self.Stocks - self.FrozenStocks


@dataclass
class Position:
    Info: dict                # 原始数据
    Type: int = 0
    MarginLevel: int = 0
    Margin: float = 0
    Amount: float = 0            # 总持仓数量
    FrozenAmount: float = 0      # 冻住的数量
    Price: float = 0         #
    Profit: float = 0
    ContractType: str = ""
    Symbol: str = ''                # 交易标的
    cost_basis: float = 0       # 持仓成本
    data_source :str = ""       # 数据来源
    enable_amount : float = 0   # 可用数量
    last_sale_price :float = 0  # 最新价格
    Direction:str = ""
    amount = Amount             # 总持仓数量

    def __post_init__(self) -> None:
        """"""
        if self.data_source == 'ptrade':
            self.symbol = self.Info['sid']
            self.amount = self.Info['amount']
            self.enable_amount = self.Info['enable_amount']
            self.cost_basis = self.Info['cost_basis']
        elif self.data_source == "tiger":
            pass

    def update_tiger(self,position):
        if position != []:
            self.Info = position
            self.symbol = position.contract.symbol
            self.Amount = position.quantity  # 总支持仓
            self.enable_amount = position.quantity  # 可卖数量
            self.cost_basis = position.average_cost  # 持仓成本
            self.last_sale_price = position.market_price

    def update(self, position:dict):
        """更新数据"""
        self.Info = position
        if self.data_source == 'ptrade':
            self.symbol = self.sid = position.sid
            self.amount = position.amount  # 总支持仓
            self.enable_amount = position.enable_amount # 可卖数量
            self.cost_basis = position.cost_basis
            self.last_sale_price = position.last_sale_price
            # order_pct = 0.5
            # A = self.amount  * order_pct



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
