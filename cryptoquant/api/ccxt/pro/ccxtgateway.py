"""
=========================================================
* Powered by StudyQuant 
* author: Rudy
* wechat:studyquant88
=========================================================
* Product Page: https://studyquant.com
* Copyright 2021 StudyQuant
* License (https://studyquant.com/)
* Coded by https://studyquant.com
=========================================================
* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
"""
from cryptoquant.trader.utility import round_to
from cryptoquant.app.datamodel.constant import (
    Product,
    OrderStatus,
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
    OrderRequest,
    MarketOrder,
    Depth,
    Account,
    Position,
)
import ccxt
import pandas as pd
from cryptoquant.config.config import binance_api_key, binance_secret_key
from cryptoquant.app.datamodel import Order
from typing import Dict, List
import time
from squtils.trader import sync_current_minute

ORDERTYPE_CCXT: Dict[OrderType, str] = {
    OrderType.LIMIT.value: "limit",
    OrderType.MARKET.value: "market",
}

ORDERTYPE_BINANCEF2VT: Dict[str, OrderType] = {v: k for k, v in ORDERTYPE_CCXT.items()}

DIRECTION_CCXT: Dict[Direction, str] = {
    Direction.LONG.value: "buy",
    Direction.SHORT.value: "sell",
}


class CcxtGateway:
    """
    通过CCXT 获取行情，交易所数据的类
    """

    def __init__(self, symbol, apikey, secret, setting={}):
        self.exchange = ccxt.binance(
            {
                "apiKey": apikey,
                "secret": secret,
                "timeout": 30000,
                "enableRateLimit": True,
                "options": {"recvWindow": 50000},
            }
        )
        self.symbol = symbol
        self.exchange_name = self.gateway_name = Exchange.BINANCE
        print("CCXT GateWay Init")

    def GetTicker(self, symbol) -> Ticker:
        """
        获取TICKER数据
        {
            Info    : {...},             // 请求交易所接口后，交易所接口应答的原始数据，回测时无此属性
            High    : 1000,              // 最高价
            Low     : 500,               // 最低价
            Sell    : 900,               // 卖一价
            Buy     : 899,               // 买一价
            Last    : 900,               // 最后成交价
            Volume  : 10000000,          // 最近成交量
            Time    : 1567736576000      // 毫秒级别时间戳
        }
        """
        if self.exchange.has["fetchTicker"]:
            data = self.exchange.fetch_ticker(symbol)
            dict_data = {
                "Info": data,
                "Open": float(data["open"]),
                "High": float(data["high"]),
                "Low": float(data["low"]),
                "Sell": float(data["ask"]),
                "Buy": float(data["bid"]),
                "Last": float(data["last"]),
                "Volume": float(data["quoteVolume"]),
                "Time": float(data["timestamp"]),
            }
            ticker = Ticker(
                symbol=symbol,
                exchange=self.exchange_name,
                datetime=data["datetime"],
                Info=data["info"],
                Time=data["timestamp"],
                High=data["high"],
                Low=data["low"],
                Sell=data["ask"],
                Buy=data["bid"],
                Last=data["last"],
                Volume=data["baseVolume"],
            )
            return ticker
        else:
            return False

    def GetDepth(self, symbol, depth=5) -> Depth:
        """
        获取TICKER数据
        """
        orderbook = self.exchange.fetch_order_book(symbol)
        asks = orderbook["asks"]
        bids = orderbook["bids"]
        Time = orderbook["timestamp"]
        depth = Depth(Asks=asks, Bids=bids, Time=Time)
        return depth

    def handle_kline_event(exchange, time_frame):
        """
        :param time_frame:  策略周期
        :return:
        """
        while True:
            try:
                kline_df = exchange.GetKline(time_frame)
                # 确保当前的最新K线时间 和 当前分钟线一致
                if kline_df["timestamp"].iloc[-1].minute == sync_current_minute(
                    time_frame
                ):
                    # print('最新K线')
                    # print(kline_df)
                    break
                else:
                    continue
                # 判断是否包含最新的数据
            except Exception as err:
                time.sleep(1)
                print(err)
            break

    def handle_kline_event(strategy, exchange, time_frame):
        """
        :param time_frame:  策略周期
        :return:
        """
        while True:
            try:
                kline_df = exchange.GetKline(time_frame)
                # 确保当前的最新K线时间 和 当前分钟线一致
                if kline_df["timestamp"].iloc[-1].minute == sync_current_minute(
                    time_frame
                ):
                    # print('最新K线')
                    # print(kline_df)
                    break
                else:
                    continue
                # 判断是否包含最新的数据
            except Exception as err:
                time.sleep(1)
                print(err)
            break
        strategy.on_kline(kline_df)

    def GetKline(self, symbol, timeframe="1m") -> pd.DataFrame:
        """get k-line data"""
        while True:
            try:
                data = self.exchange.fetch_ohlcv(symbol, timeframe)
                kline_df = pd.DataFrame(data)
                # kline_df.columns = ['time', 'open', 'high', 'low', 'close', 'volume']
                kline_df.columns = ["time", "open", "high", "low", "close", "volume"]
                kline_df.loc[:, "localminute"] = kline_df["time"].apply(
                    lambda x: time.localtime(int(x / 1000))
                )
                kline_df.loc[:, "timestamp"] = kline_df["localminute"].apply(
                    lambda x: time.strftime("%Y-%m-%d %H:%M:%S", x)
                )
                kline_df["timestamp"] = pd.to_datetime(kline_df["timestamp"])
                df = kline_df[["timestamp", "open", "high", "low", "close", "volume"]]

                if kline_df["timestamp"].iloc[-1].minute == sync_current_minute(
                    timeframe
                ):
                    break
                else:
                    continue

            except Exception as err:
                print(err)
                return False

        return df

    def GetAccount(self, symbol) -> Account:
        """
        获取账户信息
        originaldata = {'code': 200,
        'data': {'XRP': {'frozen': '0', 'available': '30'},
        'USDT': {'frozen': '0', 'available': '33.57922'}}}
        :return: all asset data
        class Account():
            Info: dict
            Balance: float = 0
            FrozenBalance: float = 0
            Stocks: float = 0
            FrozenStocks: float = 0
        """
        coin_name, quote_name = symbol.split("/")
        """
        You need to
        synchronize your clock with a time server to keep up with them
        or you can add a recvWindow extra param, like so:
        """
        data = self.exchange.fetch_balance({"recvWindow": 50000})
        coin_data = data[coin_name]
        quote_data = data[quote_name]
        account = Account(
            Info=data,
            Balance=quote_data["free"],
            FrozenBalance=quote_data["used"],
            Stocks=coin_data["free"],
            FrozenStocks=coin_data["used"],
        )
        return account

    def GetOpenOrders(self, symbol) -> List[Order]:
        # 获取未成交订单
        open_orders = self.exchange.fetchOpenOrders(symbol=symbol)
        # print('open_orders',open_orders)
        print("all_orders", open_orders)
        all_orders_object = []
        for order in open_orders:
            order_object = self.ccxtorder_to_studyquant_order(order)
            all_orders_object.append(order_object)
        return all_orders_object

    def GetOrders(self, symbol) -> List[Order]:
        # 获取所有订单
        all_orders = self.exchange.fetchOrders(symbol=symbol)
        # 获取全部订单
        print("all_orders", all_orders)
        all_orders_object = []
        for order in all_orders:
            order_object = self.ccxtorder_to_studyquant_order(order)
            all_orders_object.append(order_object)

        return all_orders_object

    def GetOrder(self, id, symbol) -> Order:
        """
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
        """
        # 获取指定订单
        order = self.exchange.fetchOrder(id=id, symbol=symbol)
        price = order["price"]
        Amount = order["amount"]
        DealAmount = order["filled"]
        AvgPrice = order["average"]

        if order["side"] == "buy":
            direction = Direction.ORDER_TYPE_BUY.value
            Offset = OrderOffset.OPEN.value
        elif order["side"] == "sell":
            direction = Direction.ORDER_TYPE_SELL.value
            Offset = OrderOffset.CLOSE.value

        if order["status"] == "open":
            Status = OrderStatus.ORDER_STATE_PENDING.value
        elif order["status"] == "closed":
            Status = OrderStatus.ORDER_STATE_CLOSED.value
        elif order["status"] == "canceled":
            Status = OrderStatus.ORDER_STATE_CANCELED.value
        elif order["status"] == "expired":
            Status = OrderStatus.ORDER_STATE_UNKNOWN.value
        else:
            self.log("不明ORDER STATUS", order["status"])

        order_instance = Order(
            Info=order["info"],
            Id=order["id"],
            Status=Status,
            Type=direction,
            Offset=Offset,
            Price=price,
            Amount=Amount,
            DealAmount=DealAmount,
            AvgPrice=AvgPrice,
            ContractType=Product.SPOT.value,
        )
        return order_instance

    def Buy(self, Price, Amount, OrderType=OrderType.LIMIT):

        return self.SendOrder(
            Symbol=self.symbol,
            Price=Price,
            Amount=Amount,
            Direction=Direction.LONG,
            OrderType=OrderType.LIMIT,
        )

    def Sell(self, Price, Amount, OrderType=OrderType.LIMIT):
        return self.SendOrder(
            Symbol=self.symbol,
            Price=Price,
            Amount=Amount,
            Direction=Direction.LONG,
            OrderType=OrderType.LIMIT,
        )

    def SendOrder(
        self,
        Symbol,
        Price,
        Amount,
        Direction: Direction,
        OrderType: OrderType = OrderType.LIMIT,
        Offset: Offset = Offset.OPEN,
    ) -> Order:
        """
        send trade order
        """
        req = OrderRequest(
            symbol=Symbol,
            exchange=Exchange.BINANCE,
            direction=Direction,
            offset=Offset,
            type=OrderType,
            price=Price,
            volume=Amount,
        )
        return self.send_order(req)

    def CancelOrder(self, id):
        """
        cancel order
        """
        try:
            cancel_info = self.exchange.cancel_order(id, self.symbol)
            if cancel_info["status"] == "canceled":
                return True
            else:
                return False
        except Exception as err:
            print(err)
            return False

    def GetTrades(self, symbol) -> List[Trade]:
        """
        获取当前交易对、合约对应的市场的交易历史（非自己），返回值：Trade结构体数组。
        Trade
        Id: int
        Time: int
        Price: float = 0
        Amount: float = 0
        Type: int = 0
        # Time = time.time()
        # since = int(round(Time * 1000)) - 86400000
        """
        data = self.exchange.fetch_trades(symbol)
        trades_list = []
        for trade in data:
            trade_object = Trade(
                Id=trade["id"],
                Time=trade["timestamp"],
                Price=trade["price"],
                Amount=trade["amount"],
                Type=Direction.ORDER_TYPE_BUY,
            )
            trades_list.append(trade_object)
        return trades_list

    def send_order(self, req: OrderRequest) -> Order:
        """
        发送下单指令
        :param req:  请求的CLASS
        :return: 数据
        """

        side = DIRECTION_CCXT[req.direction.value]
        order_type = ORDERTYPE_CCXT[req.type.value]
        symbol = req.symbol
        amount = req.volume
        price = req.price
        order = self.exchange.create_order(symbol, order_type, side, amount, price)
        new_order = self.ccxtorder_to_studyquant_order(order)
        return new_order

    def ccxtorder_to_studyquant_order(self, order):
        """change ccxt order data sttructure to studyquant order"""

        price = order["price"]
        Amount = order["amount"]
        DealAmount = order["filled"]
        AvgPrice = order["average"]

        if order["side"] == "buy":
            direction = Direction.ORDER_TYPE_BUY.value
            Offset = OrderOffset.OPEN.value
        elif order["side"] == "sell":
            direction = Direction.ORDER_TYPE_SELL.value
            Offset = OrderOffset.CLOSE.value

        if order["status"] == "open":
            Status = OrderStatus.ORDER_STATE_PENDING.value
        elif order["status"] == "closed":
            Status = OrderStatus.ORDER_STATE_CLOSED.value
        elif order["status"] == "canceled":
            Status = OrderStatus.ORDER_STATE_CANCELED.value
        elif order["status"] == "expired":
            Status = OrderStatus.ORDER_STATE_UNKNOWN.value
        else:
            self.write_log("不明ORDER STATUS", order["status"])

        order_instance = Order(
            Info=order["info"],
            Id=order["id"],
            Status=Status,
            Type=direction,
            Offset=Offset,
            Price=price,
            Amount=Amount,
            DealAmount=DealAmount,
            AvgPrice=AvgPrice,
            ContractType=Product.SPOT.value,
        )
        return order_instance


if __name__ == "__main__":
    pass
    apikey = binance_api_key
    secret = binance_secret_key
    symbol = "EOS/USDT"
    trade_api = CcxtGateway(symbol, apikey, secret)
    print(trade_api)
    print(trade_api.exchange)
    # print("GEt Trades", trade_api.GetTrades(symbol))
    print(trade_api.GetTicker(symbol))
    # print(trade_api.GetDepth(symbol))
    # print(trade_api.GetAccount(symbol)
    print("获取K线", trade_api.GetKline(symbol))
    print("get Orders", trade_api.GetOrders(symbol))
    print("get open Orders", trade_api.GetOpenOrders(symbol))

    # 买单
    buy_order = trade_api.Buy(Price=3, Amount=4)
    print(f"获取订单{trade_api.GetOrder(buy_order.id,symbol)}")

    # 撤单
    cancel_order = trade_api.CancelOrder(buy_order.id)
    print(f"取消订单{cancel_order}")

    # 卖单
    sell_order = trade_api.Sell(Price=5, Amount=4)
    print(f"获取订单{trade_api.GetOrder(buy_order.id,symbol)}")

    # 撤单
    cancel_order = trade_api.CancelOrder(sell_order.id)
    print(f"取消订单{cancel_order}")
