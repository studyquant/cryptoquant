# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         okex_gateway
# Description:  
# Author:       Rudy
# U:            project
# Date:         2020-07-07
#-------------------------------------------------------------------------------
"""
web:  studyquant.com
author: Rudy
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
from cryptoquant.api.okex.spot_api import SpotAPI
import time
import pandas as pd
from cryptoquant.app.cta_strategy import (
    CtaTemplate,
    StopOrder,
    TickData,
    BarData,
    TradeData,
    OrderData,
    BarGenerator,
    ArrayManager,
)
import pytz

from datetime import datetime
from cryptoquant.trader.object import AccountData,OrderRequest,OrderType
from cryptoquant.trader.utility import load_json, save_json, extract_vt_symbol, round_to
from threading import Lock

DIRECTION_VT2OKEX = {Direction.LONG: "buy", Direction.SHORT: "sell"}
DIRECTION_OKEX2VT = {v: k for k, v in DIRECTION_VT2OKEX.items()}
ORDERTYPE_VT2OKEX = {
    OrderType.LIMIT: "limit",
    OrderType.MARKET: "market"
}

CHINA_TZ = pytz.timezone("Asia/Shanghai")

# 做一个中间通用的接口来方便策略类来调用。
class OkexSpotApi():
    """
    Okex REST API
    """
    exchange_name = Exchange.OKEX
    author = 'StudyQuant'

    def __init__(self,api):
        """
        初始化方法
        :param api:  原交易所的API
        :return:None
        """
        self.connect_time = datetime.now().strftime("%y%m%d%H%M%S")
        # self.order_manager = LocalOrderManager(self, self.connect_time)
        self.order_count_lock = Lock()
        self.order_count = 0
        self.exchange = api

    def connect(self, setting:dict) -> None:
        """
        连接API KEY SECRET
        :param setting:  账户设置
        :return:None
        """
        key = setting["key"]
        secret = setting["secret"]
        passphrase = setting["passphrase"]
        self.exchange = SpotAPI(key, secret, passphrase,True)
        print('OKex spot gateway connected')

    def get_coin_account_info(self,coin):
        """
        获取当前币的账户信息
        :param coin:  币种
        :return:AccountData
        """
        coin_account_info = self.exchange.get_coin_account_info(coin)  # 获取币的信息
        account_data = AccountData(accountid = 'okex',
                    balance = float(coin_account_info['balance']),
                    frozen = float(coin_account_info['frozen']),
                    gateway_name = self.exchange_name
                    )
        return account_data

    def GetTicker(self, symbol)-> dict:
        """
        获取最新价格
        :return:TickData
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
        ticker = self.exchange.get_specific_ticker(symbol)
        ticker_data = TickData(
            symbol=symbol,
            exchange=Exchange.OKEX,
            datetime=datetime.now(CHINA_TZ),
            gateway_name=self.exchange_name,
            last_price = ticker['last'],
            last_volume = ticker['last_qty']
        )
        return ticker_data

    def get_kline_data(self, symbol, time_frame) -> pd.DataFrame:
        """
        获取K线数据DF
        获取当前币的账户信息
        :param symbol:  交易Symbol
        :param time_frame: 时间周期
        :return:Kline dataframe
        """
        if time_frame == '1m':
            time_frame2 = 60

        elif time_frame == '5m':
            time_frame2 = 300

        elif time_frame == '15m':
            time_frame2 = 900

        elif time_frame == '30m':
            time_frame2 = 1800

        elif time_frame == '1h':
            time_frame2 = 3600

        elif time_frame == '1d':
            time_frame2 = 86400

        kline = self.exchange.get_kline(symbol,time_frame2, '', '')
        kline = pd.DataFrame(kline)
        kline.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        kline.index = pd.to_datetime(kline.timestamp)
        kline = kline.sort_index(ascending=True)
        del kline['timestamp']
        #        kline = kline.drop(columns=['timestamp'])
        kline = pd.DataFrame(kline, dtype=float)
        return kline

    def create_order(self, instrument_id, order_price, size, side,type, order_type = '0', client_oid = ''):
        '''
        限价卖出
        instrument_id： symbol
        order_price : 价格
        size ： 成交量 - 限价单，  市价单，成交金额
        side:买卖方向,buy or sell
        type: 下单类型
        order_type: 	参数填数字
        0：普通委托（order type不填或填0都是普通委托）
        1：只做Maker（Post only）
        2：全部成交或立即取消（FOK）
        3：立即成交并取消剩余（IOC）
        '''
        if type == 'limit':
            data = self.exchange.take_order(
                instrument_id, side, client_oid=client_oid, type= type, size=size, price=order_price, order_type=order_type,
                notional='')

        elif type == 'market':
            # 如果是市价单，SIZE填写为 金额
            data = self.exchange.take_order(
                instrument_id, side, client_oid=client_oid, type= type, size=size, price=order_price, order_type=order_type,
                notional= size)
        else:
            data = []
        print(data)
        return data


    def send_template_order(self,
                            symbol,
                            Direction,
                            Offset,
                            price: float,
                            volume: float,
                            stop: bool = False,
                            lock: bool = False,
                            orderid = '',
                            order_type = OrderType.LIMIT
                            ):
        """
        symbol, Direction.LONG, Offset.CLOSE, price, volume, stop, lock
        Args:
            symbol:
            price:
            volume:
            stop:
            lock:

        Returns:

        """
        req = OrderRequest(symbol=symbol,
                           offset=Offset,
                           exchange=self.exchange_name,
                           direction=Direction,
                           type=order_type,
                           price=price,
                           volume=volume,
                           orderid=orderid,
                           )
        print(req)
        return self.send_serve_order(req)


    def send_order(
        self,
        strategy: CtaTemplate,
        direction: Direction,
        offset: Offset,
        price: float,
        volume: float,
        stop: bool = False,
        lock: bool = False,
        customize_order_id:str = '',
        order_type = OrderType.LIMIT,
    ):
        """
        下单
        :param direction: direction 方向
        :param offset: 开仓 还是 平仓
        :param price: price
        :param volume: volume
        :param stop: 是否是停损单
        :param lock: 是否锁仓
        :param customize_order_id: orderId
        :param order_type: limit_order or market_order
        :return: orderId
        """
        # contract = self.main_engine.get_contract(strategy.vt_symbol)
        # if not contract:
        #     self.write_log(f"委托失败，找不到合约：{strategy.vt_symbol}", strategy)
        #     return ""
        # # Round order price and volume to nearest incremental value
        # price = round_to(price, contract.pricetick)
        # volume = round_to(volume, contract.min_volume)
        req = OrderRequest(symbol = strategy.symbol,
                         offset = offset,
                         exchange = Exchange.OKEX,
                         direction = direction,
                         type = order_type,
                         price = price,
                         volume = volume
                         )
        return self.send_serve_order(req)

    def cancel_orders(self,instrument_id):
        """
        取消所有目标币种订单
        """
        # orders = self.exchange.get_orders_list(instrument_id)

        # 获取未成交订单
        orders_pending = self.exchange.get_orders_pending(instrument_id)
        if orders_pending != []:
            df = pd.DataFrame(orders_pending)
            # 获取目标币种的订单号
            order_id_list = list(df[df['instrument_id'] == instrument_id]['order_id'])

            # 批量取消订单
            params = {'instrument_id': instrument_id, 'order_ids': order_id_list}
            data = self.exchange.revoke_orders([params])
            print(data)
        else:
            print('无委托订单')
            data = []
        return data

    # def send_server_order(
    #     self,
    #     strategy: CtaTemplate,
    #     contract: ContractData,
    #     direction: Direction,
    #     offset: Offset,
    #     price: float,
    #     volume: float,
    #     type: OrderType,
    #     lock: bool
    # ):
    #     """
    #     Send a new order to server.
    #     """
    #     # Create request and send order.
    #     original_req = OrderRequest(
    #         symbol=contract.symbol,
    #         exchange=contract.exchange,
    #         direction=direction,
    #         offset=offset,
    #         type=type,
    #         price=price,
    #         volume=volume,
    #         reference=f"{APP_NAME}_{strategy.strategy_name}"
    #     )
    #
    #     # Convert with offset converter
    #     req_list = self.offset_converter.convert_order_request(original_req, lock)
    #
    #     # Send Orders
    #     vt_orderids = []
    #
    #     for req in req_list:
    #         vt_orderid = self.main_engine.send_order(
    #             req, contract.exchange_name)
    #
    #         # Check if sending order successful
    #         if not vt_orderid:
    #             continue
    #
    #         vt_orderids.append(vt_orderid)
    #         self.offset_converter.update_order_request(req, vt_orderid)
    #         # Save relationship between orderid and strategy.
    #         self.orderid_strategy_map[vt_orderid] = strategy
    #         self.strategy_orderid_map[strategy.strategy_name].add(vt_orderid)
    #
    #     return vt_orderids
    #

    def send_serve_order(self,req):
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

        order = req.create_order_data(orderid, self.exchange_name)
        # 发送订单
        data = self.create_order( instrument_id = req.symbol,
                                   order_price = req.price,
                                   size = req.volume,
                                   type = data['type'],
                                   side = data['side'],
                                   client_oid = req.orderid
                                   )
        # if data['result']:
        #     self.on_order(order)
        return data

    def _new_order_id(self):
        with self.order_count_lock:
            self.order_count += 1
            return self.order_count

    # def GetDepth(self):
    #     """
    #     :return:
    #     """
    #
    # def GetTrades(self):
    #
    #
    # def GetTrades(self):
    #
    #
    # def Buy(self, Price, Amount):
    #
    #
    # #------- 账户信息--------------
    # def GetAccount(self):
    #
    #
    # def GetName(self):
    #
    # def get_balance(self,symbol):
    #     pass
    #
    # def get_kline(self,symbol,minutes):
    #     """
    #     get kline data
    #     :param symbol:
    #     :param minutes:
    #     :return:
    #     """
    #     data = self.request_client.spot_kline(symbol, minutes)
    #     final = {symbol:data}
    #     self.on_kline(final)
    #     return data
    #



if __name__=="__main__":
    from cryptoquant.config.config import ok_api_key, ok_seceret_key, ok_passphrase
    crypto_setting = {
        "key": ok_api_key,
        "secret": ok_seceret_key,
        "passphrase":ok_passphrase,
        "session_number": 3,
        "proxy_host": "",
        "proxy_port": 0,
    }
    symbol = 'OKB-USDT'
    minutes = '5m'

    api = SpotAPI(ok_api_key, ok_seceret_key, ok_passphrase,True)
    exchange = OkexSpotApi(api)
    # OkexRestApi.connect(crypto_setting)

    # 获取币对的账户信息
    # coin = symbol.split('-')[0]
    # account_info = exchange.get_coin_account_info(coin)
    # # 获取TICK
    # tick_data = exchange.GetTicker(symbol)
    # # 获取K线
    # kline_data = exchange.get_kline_data(symbol,minutes)
    # # 下单
    # original_req = OrderRequest(symbol = symbol,
    #             exchange = Exchange.OKEX,
    #             direction = Direction.LONG,
    #             offset = Offset.OPEN,
    #             type = OrderType.MARKET,
    #             price = 3,
    #             volume = 6,
    #             orderid = 'su')

    cancel_order = exchange.cancel_order(symbol)
    cancel_order



    # order_data = exchange.send_serve_order(original_req)
    # print(order_data)




    # usdt = OkexRestApi.get_balance('usdt')
    # 获取持仓
    # pos = OkexRestApi.get_position(symbol)



    
    
    
    
    
    
"""
好好学习，天天向上。 
project
"""