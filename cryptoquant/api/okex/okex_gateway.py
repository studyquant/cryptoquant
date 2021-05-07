# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         okex_gateway
# Description:  
# Author:       Rudy
# U:            project
# Date:         2020-07-07
#-------------------------------------------------------------------------------

"""
好好学习，天天向上。 
Mark:project
"""
from cryptoquant.trader.object import OrderRequest
from cryptoquant.trader.constant import (
    Direction,
    OrderType,
    Interval,
    Exchange,
    Offset,
    Status)
from cryptoquant.trader.engine import Event, EventEngine
from cryptoquant.trader.base_gateway import BaseGateway, LocalOrderManager
from cryptoquant.trader.object import (
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
    HistoryRequest
)
from datetime import datetime, timedelta
from cryptoquant.api.okex.okex_v3_spot import OkexSpotV3
from cryptoquant.api.okex.setting import api_key, seceret_key, passphrase
import pandas as pd

DIRECTION_VT2OKEX = {Direction.LONG: "buy", Direction.SHORT: "sell"}
DIRECTION_OKEX2VT = {v: k for k, v in DIRECTION_VT2OKEX.items()}
ORDERTYPE_VT2OKEX = {
    OrderType.LIMIT: "limit",
    OrderType.MARKET: "market"
}

ORDERTYPE_OKEX2VT = {v: k for k, v in ORDERTYPE_VT2OKEX.items()}


from threading import Lock


class OkexSpotApi(BaseGateway):
    """
    BINANCE REST API
    """
    author = 'StudyQuant'
    def __init__(self, event_engine: EventEngine):
        """Constructor"""
        super().__init__(event_engine, "OKEX")
        self.connect_time = datetime.now().strftime("%y%m%d%H%M%S")
        self.order_manager = LocalOrderManager(self, self.connect_time)


        self.order_count_lock = Lock()
        self.order_count = 10000
        # self.order_manager.on_order(order)

    def connect(self, setting:dict):
        """连接API KEY SECRET"""
        key = setting["key"]
        secret = setting["secret"]
        passphrase = setting["passphrase"]
        # session_number = setting["session_number"]
        # server = setting["server"]
        # proxy_host = setting["proxy_host"]
        # proxy_port = setting["proxy_port"]
        self.request_client = OkexSpotV3(api_key, seceret_key, passphrase,True)
        print('OKex spot gateway connected')
        # self.event_engine.register(EVENT_TIMER, self.process_timer_event)


    def get_position(self,symbol):
        """获取币对信息"""
        position_info = self.request_client.account_info(symbol)  # 获取币的信息
        # usdt = self.account_info('usdt')
        coin = float(position_info['available'])   # 可用币
        return coin


    def get_ticker(self, symbol = None):
        """
        获取最新价格
        :param symbol:
        :param minutes:
        :return:
        {
          "symbol": "LTCBTC",       // 交易对
          "price": "4.00000200"     // 价格
        }
        """
        result = self.request_client.spot_ticker(symbol=symbol)
        if len(result)>1:
            # self.on_tick(result)
            return result


    def get_balance(self,symbol):
        pass


    def get_kline(self,symbol,minutes):
        """
        get kline data
        :param symbol:
        :param minutes:
        :return:
        """
        data = self.request_client.spot_kline(symbol, minutes)
        final = {symbol:data}
        self.on_kline(final)
        return data

    def cancel_order(self):
        """

        """
        return

    def _new_order_id(self):
        with self.order_count_lock:
            self.order_count += 1
            return self.order_count

    def send_order(self,req):
        """
        发送下单指令
        :param req:  请求的CLASS
        :return: orderid
        """
        orderid = f"a{self.connect_time}{self._new_order_id()}"
        # order_id = self.order_manager.new_local_orderid()
        data = {
            "client_oid": orderid,
            "type": ORDERTYPE_VT2OKEX[req.type],
            "side": DIRECTION_VT2OKEX[req.direction],
            "instrument_id": req.symbol
        }

        if req.type == OrderType.MARKET:
            if req.direction == Direction.LONG:
                data["notional"] = req.volume
            else:
                data["size"] = req.volume
        else:
            data["price"] = req.price
            data["size"] = req.volume

        order = req.create_order_data(orderid, self.gateway_name)
        # 发送订单
        data = self.request_client.spot_order( instrument_id = req.symbol,
                                               order_price = req.price,
                                               size = data['size'],
                                               order_type = data['type'],
                                               side = data['side'],
                                               client_oid = data['client_oid']
                                               )

        if data['result']:
            self.on_order(order)

        return order.vt_orderid

if __name__=="__main__":
    crypto_setting = {
        "key": api_key,
        "secret": seceret_key,
        "passphrase":passphrase,
        "session_number": 3,
        "proxy_host": "",
        "proxy_port": 0,
    }

    symbol = 'OKB-USDT'
    minutes = '5m'
    event_engine = EventEngine()
    OkexRestApi = OkexSpotApi(event_engine)
    OkexRestApi.connect(crypto_setting)
    # 获取TICK
    tick_data = OkexRestApi.get_ticker(symbol)
    # 获取K线
    # kline_data = OkexRestApi.get_kline(symbol,minutes)


    # 下单
    original_req = OrderRequest(symbol = symbol,
                exchange = Exchange.OKEX,
                direction = Direction.SHORT,
                offset = Offset.OPEN,
                type = OrderType.LIMIT,
                price = 2,
                volume = 1)


    # order_data = OkexRestApi.send_order(original_req)
    # print(order_data)




    # usdt = OkexRestApi.get_balance('usdt')




    # 获取持仓
    # pos = OkexRestApi.get_position(symbol)

    
    
    
    
    
    
"""
好好学习，天天向上。 
project
"""