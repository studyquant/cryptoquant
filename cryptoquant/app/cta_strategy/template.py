""""""
from abc import ABC
from copy import copy
from typing import Any, Callable

from cryptoquant.app.datamodel.constant import Interval,  Offset,Direction,Exchange
from cryptoquant.app.datamodel.object import BarData, TickData, OrderData, TradeData, OrderType,OrderRequest
from cryptoquant.trader.utility import virtual
# from cryptoquant.app.datamodel.constant import Direction
from datetime import datetime

# from cryptoquant.app.cta_strategy.api_gateway import fmz_template
from .base import StopOrder, EngineType


class CtaTemplate(ABC):
    """策略的基类"""

    author = ""
    parameters = []
    variables = []
    pos = 0
    gateway_name = Exchange.LOCAL
    def __init__(
        self,
        cta_engine: Any,
        strategy_name: str,
        vt_symbol: str,
        setting: dict,
    ):
        """"""
        self.cta_engine = cta_engine  # 也可以是交易所API
        self.strategy_name = strategy_name
        self.vt_symbol = vt_symbol
        # self.gateway = fmz_template(cta_engine)  # 交易所
        self.inited = False
        self.trading = False
        self.pos = 0

        # Copy a new variables list here to avoid duplicate insert when multiple
        # strategy instances are created with the same strategy class.
        self.variables = copy(self.variables)
        self.variables.insert(0, "inited")
        self.variables.insert(1, "trading")
        self.variables.insert(2, "pos")

        self.update_setting(setting)

    def update_setting(self, setting: dict):
        """
        Update strategy parameter wtih value in setting dict.
        """
        for name in self.parameters:
            if name in setting:
                setattr(self, name, setting[name])

    @classmethod
    def get_class_parameters(cls):
        """
        Get default parameters dict of strategy class.
        """
        class_parameters = {}
        for name in cls.parameters:
            class_parameters[name] = getattr(cls, name)
        return class_parameters

    def get_parameters(self):
        """
        Get strategy parameters dict.
        """
        strategy_parameters = {}
        for name in self.parameters:
            strategy_parameters[name] = getattr(self, name)
        return strategy_parameters

    def get_variables(self):
        """
        Get strategy variables dict.
        """
        strategy_variables = {}
        for name in self.variables:
            strategy_variables[name] = getattr(self, name)
        return strategy_variables

    def strategy_report_markdown(self,title = ""):
        data = self.get_data()
        msg = f"## {title} \n" \
              f"策略名称：{data['strategy_name']} \n" \
              f"当前价格:{data['variables']['current_price']} \n" \
              f"当前信号：{data['variables']['signal']} \n" \
              f"当前持仓:{data['variables']['pos']} \n" \
              f"## 策略参数 \n " \
              f"{data['parameters']}\n" \
              f"\n" \
              f"## 策略变量 \n" \
              f"{data['variables']} \n" \
              f"{datetime.now()}"
        return msg
    def get_data(self):
        """
        Get strategy data.
        """
        strategy_data = {
            "strategy_name": self.strategy_name,
            "vt_symbol": self.vt_symbol,
            "class_name": self.__class__.__name__,
            "author": self.author,
            "parameters": self.get_parameters(),
            "variables": self.get_variables(),
        }
        return strategy_data

    @virtual
    def on_init(self):
        """
        Callback when strategy is inited.
        """
        pass

    @virtual
    def on_start(self):
        """
        Callback when strategy is started.
        """
        pass

    @virtual
    def on_stop(self):
        """
        Callback when strategy is stopped.
        """
        pass

    @virtual
    def on_tick(self, tick: TickData):
        """
        Callback of new tick data update.
        """
        pass

    @virtual
    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """
        pass

    @virtual
    def on_trade(self, trade: TradeData):
        """
        Callback of new trade data update.
        """
        pass

    @virtual
    def on_order(self, order: OrderData):
        """
        Callback of new order data update.
        """
        pass

    @virtual
    def on_stop_order(self, stop_order: StopOrder):
        """
        Callback of stop order update.
        """
        pass

    def buy(
        self,
        price: float,
        volume: float,
        stop: bool = False,
        lock: bool = False,
        order_id="",
        order_type=OrderType.LIMIT,
        skew = 0
    ):
        """
        Send buy order to open a long position.
        """
        return self.send_order(
            Direction.LONG, Offset.OPEN, price-skew, volume, stop, lock, order_id, order_type
        )

    def sell(
        self,
        price: float,
        volume: float,
        stop: bool = False,
        lock: bool = False,
        order_id="",
        order_type=OrderType.LIMIT,
        skew=0
    ):
        """
        Send sell order to close a long position.
        """
        return self.send_order(
            Direction.SHORT,
            Offset.CLOSE,
            price+skew,
            volume,
            stop,
            lock,
            order_id,
            order_type,
        )

    def short(
        self,
        price: float,
        volume: float,
        stop: bool = False,
        lock: bool = False,
        order_id="",
        order_type=OrderType.LIMIT,
        skew=0
    ):
        """
        Send short order to open as short position.
        """
        return self.send_order(
            Direction.SHORT,
            Offset.OPEN,
            price+skew,
            volume,
            stop,
            lock,
            order_id,
            order_type,
        )

    def cover(
        self,
        price: float,
        volume: float,
        stop: bool = False,
        lock: bool = False,
        order_id="",
        order_type=OrderType.LIMIT,
        skew=0
    ):
        """
        Send cover order to close a short position.
        """
        return self.send_order(
            Direction.LONG,
            Offset.CLOSE,
            price-skew,
            volume,
            stop,
            lock,
            order_id,
            order_type,
        )


    def Buy(self, price: float, volume: float, order_id='', order_type=OrderType.LIMIT,symbol=None,pos_side = Direction.LONG):
        """
        Send buy order to open a long position.
        args:
            pos_side :
        """
        req = self.get_order_request(price= price, volume=volume,  direction=Direction.LONG, order_id=order_id, pos_side=pos_side,order_type=order_type,offset=Offset.OPEN)
        order = self.send_order_by_req(req)
        return order

    def Sell(self, price: float, volume: float, order_id='', order_type=OrderType.LIMIT,symbol=None,pos_side = Direction.SHORT):
        """
        Send buy order to open a long position.
        args:
            pos_side :
        """
        req = self.get_order_request(price= price, volume=volume,  direction=Direction.SHORT, order_id=order_id, pos_side=pos_side,order_type=order_type,offset=Offset.CLOSE)
        order = self.send_order_by_req(req)
        return order

    def SellShort(self, price: float, volume: float, order_id='', order_type=OrderType.LIMIT,symbol=None,pos_side = Direction.SHORT):
        """
        Send buy order to open a long position.
        args:
            pos_side :
        """
        req = self.get_order_request(price= price, volume=volume,  direction=Direction.LONG, order_id=order_id, pos_side=pos_side,order_type=order_type,offset=Offset.CLOSE)
        order = self.send_order_by_req(req)
        return order

    def Short(self, price: float, volume: float, order_id='', order_type=OrderType.LIMIT,symbol=None,pos_side = Direction.SHORT):
        """
        Send buy order to open a long position.
        args:
            pos_side :
        """
        req = self.get_order_request(price= price, volume=volume, direction=Direction.SHORT, order_id=order_id, pos_side=pos_side,order_type=order_type,offset=Offset.OPEN)
        order = self.send_order_by_req(req)
        return order

    def get_order_request(self,price: float, volume: float,  direction:Direction ,order_id='', symbol=None, pos_side=Direction.UNKNOWN,order_type=OrderType.LIMIT,offset=Offset.NONE):
        if not symbol:
            symbol = self.symbol
        req = OrderRequest(symbol = self.symbol,
                           exchange= self.gateway_name,
                           direction= direction,
                           type = order_type,
                           price = price,
                           volume = volume,
                           orderid = order_id,
                           offset = offset,
                           # reference= self.gateway_name,
                           pos_side = pos_side
                           )
        return req

    # def Order(self, ):


    def send_order_by_req(self,req:OrderRequest):
        if self.trading:
            order_data = self.cta_engine.send_order_by_req(req)
            self.process_order_data(order_data)
        else:
            self.write_log(f'策略状态:{self.trading}')
            order_data = None
        return order_data


    def process_order_data(self, order_data: OrderData,return_order_id_with_list = False)->OrderData:
        """
        处理返回订单数据
        Args:
            order_data:
            return_order_id_with_list:

        Returns:
        """
        if return_order_id_with_list:
            if isinstance(order_data,OrderData):
                return [order_data.orderid]  # 返回订单
            else:
                return []
        # 返回order数据类即可
        else:
            return order_data




    def send_order(
        self,
        direction: Direction,
        offset: Offset,
        price: float,
        volume: float,
        stop: bool = False,
        lock: bool = False,
        order_id: str = "",
        order_type=OrderType.LIMIT,
    ):
        """
        Send a new order.
        """
        if self.trading:
            order_data = self.cta_engine.send_order(
                self, direction, offset, price, volume, stop, lock, order_id, order_type
            )
            if isinstance(order_data,OrderData):
                return [order_data.orderid]  # 返回订单
            else:
                return []

        else:
            self.write_log('策略交易未开启')
            return []

    def cancel_order(self, vt_orderid: str):
        """
        Cancel an existing order.
        """
        if self.trading:
            self.cta_engine.cancel_order(self, vt_orderid)

    def cancel_all(self):
        """
        Cancel all orders sent by strategy.
        """
        if self.trading:
            self.cta_engine.cancel_all(self)

    def write_log(self, msg: str):
        """
        Write a log message.
        """
        self.msg = msg
        self.cta_engine.write_log(msg, self)

    def get_engine_type(self):
        """
        Return whether the cta_engine is backtesting or live trading.
        """
        return self.cta_engine.get_engine_type()

    def get_pricetick(self):
        """
        Return pricetick data of trading contract.
        """
        return self.cta_engine.get_pricetick(self)

    def load_bar(
        self,
        days: int,
        interval: Interval = Interval.MINUTE,
        callback: Callable = None,
        use_database: bool = False,
    ):
        """
        Load historical bar data for initializing strategy.
        """
        if not callback:
            callback = self.on_bar

        self.cta_engine.load_bar(self.vt_symbol, days, interval, callback, use_database)

    def load_tick(self, days: int):
        """
        Load historical tick data for initializing strategy.
        """
        self.cta_engine.load_tick(self.vt_symbol, days, self.on_tick)

    def put_event(self):
        """
        Put an strategy data event for ui update.
        """
        if self.inited:
            self.cta_engine.put_strategy_event(self)

    def send_email(self, msg):
        """
        Send email to default receiver.
        """
        if self.inited:
            self.cta_engine.send_email(msg, self)

    def sync_data(self):
        """
        Sync strategy variables value into disk storage.
        """
        if self.trading:
            self.cta_engine.sync_strategy_data(self)


class CtaSignal(ABC):
    """"""

    def __init__(self):
        """"""
        self.signal_pos = 0

    @virtual
    def on_tick(self, tick: TickData):
        """
        Callback of new tick data update.
        """
        pass

    @virtual
    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """
        pass

    def set_signal_pos(self, pos):
        """"""
        self.signal_pos = pos

    def get_signal_pos(self):
        """"""
        return self.signal_pos


class TargetPosTemplate(CtaTemplate):
    """"""

    tick_add = 1

    last_tick = None
    last_bar = None
    target_pos = 0

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)

        self.active_orderids = []
        self.cancel_orderids = []

        self.variables.append("target_pos")

    @virtual
    def on_tick(self, tick: TickData):
        """
        Callback of new tick data update.
        """
        self.last_tick = tick

        if self.trading:
            self.trade()

    @virtual
    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """
        self.last_bar = bar

    @virtual
    def on_order(self, order: OrderData):
        """
        Callback of new order data update.
        """
        vt_orderid = order.vt_orderid

        if not order.is_active():
            if vt_orderid in self.active_orderids:
                self.active_orderids.remove(vt_orderid)

            if vt_orderid in self.cancel_orderids:
                self.cancel_orderids.remove(vt_orderid)

    def check_order_finished(self):
        """"""
        if self.active_orderids:
            return False
        else:
            return True

    def set_target_pos(self, target_pos):
        """"""
        self.target_pos = target_pos
        self.trade()

    def trade(self):
        """"""
        if not self.check_order_finished():
            self.cancel_old_order()
        else:
            self.send_new_order()

    def cancel_old_order(self):
        """"""
        for vt_orderid in self.active_orderids:
            if vt_orderid not in self.cancel_orderids:
                self.cancel_order(vt_orderid)
                self.cancel_orderids.append(vt_orderid)

    def send_new_order(self):
        """"""
        pos_change = self.target_pos - self.pos
        if not pos_change:
            return

        long_price = 0
        short_price = 0

        if self.last_tick:
            if pos_change > 0:
                long_price = self.last_tick.ask_price_1 + self.tick_add
                if self.last_tick.limit_up:
                    long_price = min(long_price, self.last_tick.limit_up)
            else:
                short_price = self.last_tick.bid_price_1 - self.tick_add
                if self.last_tick.limit_down:
                    short_price = max(short_price, self.last_tick.limit_down)

        else:
            if pos_change > 0:
                long_price = self.last_bar.close_price + self.tick_add
            else:
                short_price = self.last_bar.close_price - self.tick_add

        if self.get_engine_type() == EngineType.BACKTESTING:
            if pos_change > 0:
                vt_orderids = self.buy(long_price, abs(pos_change))
            else:
                vt_orderids = self.short(short_price, abs(pos_change))
            self.active_orderids.extend(vt_orderids)

        else:
            if self.active_orderids:
                return

            if pos_change > 0:
                if self.pos < 0:
                    if pos_change < abs(self.pos):
                        vt_orderids = self.cover(long_price, pos_change)
                    else:
                        vt_orderids = self.cover(long_price, abs(self.pos))
                else:
                    vt_orderids = self.buy(long_price, abs(pos_change))
            else:
                if self.pos > 0:
                    if abs(pos_change) < self.pos:
                        vt_orderids = self.sell(short_price, abs(pos_change))
                    else:
                        vt_orderids = self.sell(short_price, abs(self.pos))
                else:
                    vt_orderids = self.short(short_price, abs(pos_change))
            self.active_orderids.extend(vt_orderids)
