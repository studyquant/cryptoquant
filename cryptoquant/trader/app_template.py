"""
=========================================================
* Powered by Flashboy
* author: Flashboy
* wechat: 
=========================================================
* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
"""
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod

from typing import Any, Sequence
from copy import copy

from cryptoquant.event import Event, EventEngine
from .event import (
    EVENT_TICK,
    EVENT_ORDER,
    EVENT_TRADE,
    EVENT_POSITION,
    EVENT_ACCOUNT,
    EVENT_CONTRACT,
    EVENT_LOG,
)
from .object import (
    TickData,
    OrderData,
    TradeData,
    PositionData,
    AccountData,
    ContractData,
    LogData,
    OrderRequest,
    CancelRequest,
    SubscribeRequest,
    HistoryRequest,
)

class AppTemplate:
    """Quant class"""
    author = "Flashboy"
    wechatid = ""
    # Fields required in setting dict for connect function.
    default_setting = {}

    # Exchanges supported in the gateway.
    exchanges = []

    def __init__(self, event_engine: EventEngine, gateway_name: str):
        """"""
        self.event_engine = event_engine
        self.gateway_name = gateway_name

    def on_event(self, type: str, data: Any = None):
        """
        General event push.
        """
        event = Event(type, data)
        self.event_engine.put(event)

    def on_tick(self, tick: TickData):
        """
        Tick event push.
        Tick event of a specific vt_symbol is also pushed.
        """
        self.on_event(EVENT_TICK, tick)
        self.on_event(EVENT_TICK + tick.vt_symbol, tick)

    def on_trade(self, trade: TradeData):
        """
        Trade event push.
        Trade event of a specific vt_symbol is also pushed.
        """
        self.on_event(EVENT_TRADE, trade)
        self.on_event(EVENT_TRADE + trade.vt_symbol, trade)

    def on_order(self, order: OrderData):
        """
        Order event push.
        Order event of a specific vt_orderid is also pushed.
        """
        self.on_event(EVENT_ORDER, order)
        self.on_event(EVENT_ORDER + order.vt_orderid, order)

    def on_position(self, position: PositionData):
        """
        Position event push.
        Position event of a specific vt_symbol is also pushed.
        """
        self.on_event(EVENT_POSITION, position)
        self.on_event(EVENT_POSITION + position.vt_symbol, position)

    def on_account(self, account: AccountData):
        """
        Account event push.
        Account event of a specific vt_accountid is also pushed.
        """
        self.on_event(EVENT_ACCOUNT, account)
        self.on_event(EVENT_ACCOUNT + account.vt_accountid, account)

    def on_log(self, log: LogData):
        """
        Log event push.
        """
        self.on_event(EVENT_LOG, log)

    def on_contract(self, contract: ContractData):
        """
        Contract event push.
        """
        self.on_event(EVENT_CONTRACT, contract)

    def write_log(self, msg: str):
        """
        Write a log event from gateway.
        """
        log = LogData(msg=msg, gateway_name=self.gateway_name)
        self.on_log(log)