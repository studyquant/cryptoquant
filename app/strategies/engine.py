""""""

import importlib
import os
import traceback
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
from copy import copy

from cryptoquant.event import Event, EventEngine
from cryptoquant.trader.engine import BaseEngine, MainEngine

from cryptoquant.trader.object import (
    OrderRequest,
    SubscribeRequest,
    HistoryRequest,
    LogData,
    TickData,
    BarData,
    ContractData
)
from cryptoquant.trader.event import (
    EVENT_TICK,
    EVENT_ORDER,
    EVENT_TRADE,
    EVENT_POSITION,
    EVENT_KLINE
)

from cryptoquant.trader.constant import (
    Direction,
    OrderType,
    Interval,
    Exchange,
    Offset,
    Status
)
# from vnpy.trader.utility import load_json, save_json, extract_vt_symbol, round_to
# from vnpy.trader.database import database_manager
# from vnpy.trader.rqdata import rqdata_client
# from vnpy.trader.converter import OffsetConverter
from cryptoquant.trader.converter import OffsetConverter

from .StrategyTemplate import CtaTemplate
EVENT_CTA_LOG = "eCtaLog"

class CtaEngine(BaseEngine):
    """"""

    # engine_type = EngineType.LIVE  # live trading engine
    setting_filename = "cta_strategy_setting.json"
    data_filename = "cta_strategy_data.json"

    def __init__(self, gateway, event_engine: EventEngine):
        """"""
        super(CtaEngine, self).__init__(gateway,event_engine,'CTA_engine')

        self.gateway = gateway
        self.strategy_setting = {}  # strategy_name: dict
        self.strategy_data = {}     # strategy_name: dict
        # 策略里面放了SYMBOL
        self.symbol_strategy_map = defaultdict(
            list)                   # vt_symbol: strategy list
        self.classes = {}           # class_name: stategy_class
        self.strategies = {}        # strategy_name: strategy
        
        # 订单里面放
        self.orderid_strategy_map = {}  # vt_orderid: strategy
        self.stop_order_count = 0   # for generating stop_orderid
        self.stop_orders = {}       # stop_orderid: stop_order

        self.init_executor = ThreadPoolExecutor(max_workers=1)
        self.rq_client = None
        self.rq_symbols = set()
        self.vt_tradeids = set()    # for filtering duplicate trade

        self.strategy_orderid_map = defaultdict(
            set)                    # strategy_name: orderid list
        
        self.offset_converter = OffsetConverter(self.main_engine)

    def add_strategy(self,strategy, strategy_name, vt_symbol, setting):
        """添加策略"""
        # strategy_class = self.classes.get(class_name, None)
        strategy = strategy(self, strategy_name, vt_symbol, setting)

        strategy.inited = True  # 加入策略，就等于初始化成功
        self.strategies[strategy_name] = strategy

        # Add vt_symbol to strategy map.
        strategies = self.symbol_strategy_map[vt_symbol]
        strategies.append(strategy)

    def init_engine(self):
        """
        """
        # self.init_rqdata()
        # self.load_strategy_class()
        # self.load_strategy_setting()
        # self.load_strategy_data()
        self.register_event()
        # self.write_log("CTA策略引擎初始化成功")

    def register_event(self):
        """注册事件"""
        self.event_engine.register(EVENT_TICK, self.process_tick_event)
        self.event_engine.register(EVENT_KLINE, self.process_kline_event)
        self.event_engine.register(EVENT_ORDER, self.process_order_event)
        # self.event_engine.register(EVENT_TRADE, self.process_trade_event)
        # self.event_engine.register(EVENT_POSITION, self.process_position_event)
        self.event_engine.start()

    def call_strategy_func(
        self, strategy: CtaTemplate, func: Callable, params: Any = None
    ):
        """
        Call function of a strategy and catch any exception raised.
        """
        try:
            if params:
                func(params)
            else:
                func()
        except Exception:
            strategy.trading = False
            strategy.inited = False

            msg = f"触发异常已停止\n{traceback.format_exc()}"
            self.write_log(msg, strategy)

    def process_kline_event(self, event: Event):
        """"""
        data = event.data
        symbol = list(data.keys())[0]
        strategies = self.symbol_strategy_map[symbol]
        if not strategies:
            return

        kline = data
        # self.check_stop_order(tick)
        for strategy in strategies:
            if strategy.inited:
                self.call_strategy_func(strategy, strategy.on_kline, kline)

    def process_tick_event(self, event: Event):
        """"""
        tick = event.data
        strategies = self.symbol_strategy_map[tick.vt_symbol]
        if not strategies:
            return

        # self.check_stop_order(tick)
        for strategy in strategies:
            if strategy.inited:
                self.call_strategy_func(strategy, strategy.on_tick, tick)

    def send_order(
        self,
        strategy: CtaTemplate,
        symbol,
        direction: Direction,
        offset: Offset,
        price: float,
        volume: float,
        stop: bool,
        lock: bool
    ):
        """
        Send new order request to a specific gateway.
        """
        original_req = OrderRequest(symbol=symbol,
                                    exchange=Exchange.BINANCE,
                                    direction=direction,
                                    offset=offset,
                                    type = OrderType.LIMIT,
                                    price=price,
                                    volume=volume)

        # Convert with offset converter
        # 目前有报错
        # req_list = self.offset_converter.convert_order_request(original_req, lock)

        # Send Orders
        vt_orderids = []

        for req in [original_req]:
            # vt_orderid = self.main_engine.send_order(
            #     req, contract.gateway_name)
            vt_orderid = self.gateway.send_order(original_req)

            # Check if sending order successful
            if not vt_orderid:
                continue

            vt_orderids.append(vt_orderid)

            # self.offset_converter.update_order_request(req, vt_orderid)
            # Save relationship between orderid and strategy.
            self.orderid_strategy_map[vt_orderid] = strategy
            self.strategy_orderid_map[strategy.strategy_name].add(vt_orderid)

        return vt_orderids

    def write_log(self, msg: str, strategy: CtaTemplate = None):
        """
        Create cta engine log event.
        """
        if strategy:
            msg = f"{strategy.strategy_name}: {msg}"

        log = LogData(msg=msg, gateway_name="CtaStrategy")
        event = Event(type=EVENT_CTA_LOG, data=log)
        self.event_engine.put(event)
        
    def process_order_event(self, event: Event):
        """"""
        print('order event')
        order = event.data

        # self.offset_converter.update_order(order)
        # 获取策略ID
        # symbol = list(data.keys())[0]

        strategy = self.orderid_strategy_map.get(order.vt_orderid, None)
        if not strategy:
            return

        # Remove vt_orderid if order is no longer active.
        vt_orderids = self.strategy_orderid_map[strategy.strategy_name]
        if order.vt_orderid in vt_orderids and not order.is_active():
            vt_orderids.remove(order.vt_orderid)

        # For server stop order, call strategy on_stop_order function
        if order.type == OrderType.STOP:
            so = StopOrder(
                vt_symbol=order.vt_symbol,
                direction=order.direction,
                offset=order.offset,
                price=order.price,
                volume=order.volume,
                stop_orderid=order.vt_orderid,
                strategy_name=strategy.strategy_name,
                status=STOP_STATUS_MAP[order.status],
                vt_orderids=[order.vt_orderid],
            )
            self.call_strategy_func(strategy, strategy.on_stop_order, so)

        # Call strategy on_order function
        self.call_strategy_func(strategy, strategy.on_order, order)
        
