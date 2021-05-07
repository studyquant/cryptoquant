
from cryptoquant.api.okex.spot_api import SpotAPI
import time
import pandas as pd


class OkexSpotV3(SpotAPI):
    # 获取当前实时K线数据
    def __init__(self,api_key, seceret_key, passphrase, server_time):
        print('OkexSpotAPI')
        SpotAPI.__init__(self, api_key, seceret_key, passphrase, server_time)

    # 行情接口
    def spot_ticker(self, symbol):
        """ get ticker 数据"""
        data = self.get_specific_ticker(symbol)
        return data

    def account_info(self,symbol):
        """获取当前币的账户信息"""
        symbol1 = symbol.split('-')[0]
        info = self.get_coin_account_info(symbol1)
        return info

    def log(self,info):
        print(info)

    # K线数据处理
    def spot_kline(self, symbol, time_frame):
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

        kline = self.get_kline(symbol,time_frame2, '', '')
        kline = pd.DataFrame(kline)
        kline.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        kline.index = pd.to_datetime(kline.timestamp)
        kline = kline.sort_index(ascending=True)
        del kline['timestamp']
        #        kline = kline.drop(columns=['timestamp'])
        kline = pd.DataFrame(kline, dtype=float)
        return kline

    def limit_buy(self, symbol, order_price, order_amount):
        '''限价买入'''
        # client_oid, otype, side, instrument_id, order_type, price = '', size = '', notional = ''
        data = self.take_order('limit', 'buy', symbol, str(order_amount), margin_trading=1, client_oid=str(1),
                               price=str(order_price), funds='')
        return data

    def limit_sell(self, symbol, order_price, order_amount):
        '''限价卖出'''
        data = self.take_order('limit', 'sell', symbol, str(order_amount), margin_trading=1, client_oid=str(1),
                               price=str(order_price), funds='')
        return data

    def spot_order(self, instrument_id, order_price, size, order_type, side, client_oid = ''):
        '''限价卖出
        side:买卖方向,buy or sell
        type: 下单类型
        '''
        # client_oid, otype, side, instrument_id, size = ''
        # take_order(self, client_oid, otype, side, instrument_id, order_type, price='', size='', notional='')

        if order_type == 'limit':
            if order_price == '':
                order_price = self.get_specific_ticker(instrument_id)['last']
            # price and size 必须填写
            data = self.take_order(
                instrument_id, side, client_oid=client_oid, type=order_type, size=size, price= order_price , order_type='0',
                notional='')
        else:
            # buy 必须填写  size
            #  必须填写
            order_price = float(self.get_specific_ticker(instrument_id)['last'])
            notional = size * order_price

            if side == 'buy':
                data = self.take_order(
                    instrument_id, side, client_oid=client_oid, type='market', size=size, price='', order_type='0',
                    notional=notional)
            else:
                data = self.take_order(
                    instrument_id, side, client_oid=client_oid, type='market', size=size, price='', order_type='0',
                    notional='')
               #sell 必须填写 notional
        print(data)
        return data


    def on_order_error(self, data):
        """失败订单处理"""
        data_dict = data.__dict__
        if data_dict['code']:
            print(data_dict['code'], data_dict['message'])
            if data_dict['code'] == 32014:
                # 有挂单Positions that you are closing exceeded the total qty of contracts allowed to close
                # result = self.get_order_list(0, '', '', '', instrument_id='ETH-USD-191227')
                if self.long_position != 0:
                    self.cancel_all(self.symbol, 'long')

                if self.short_position != 0:
                    self.cancel_all(self.symbol, 'short')
            else:
                if self.long_position != 0:
                    self.cancel_all(self.symbol, 'long')

                if self.short_position != 0:
                    self.cancel_all(self.symbol, 'short')

                # order_list = self.get_order_list('0', '', '', '100', symbol) # 获取订单列表
                # if order_list:
                #
                #
                # self.cancel_all_orders()
    def iceburg_order(self,instrument_id, side, order_type, size, algo_price, trigger_price):
        """
        instrument_id 	String 	是 	币对名称
        mode 	String 	是 	1：币币
                            2：杠杆
                            order_type 	String 	是
                            1：止盈止损
                            2：跟踪委托
                            3：冰山委托
                            4：时间加权
        size 	String 	是 	委托总数，填写值1\<=X\<=1000000的整数
        side 	String 	是 	buy 或 sell
        :return:
        """
        mode = 3
        data = self.order_algo(instrument_id, side, mode, order_type, size, algo_price, trigger_price)

if __name__ == "__main__":
    from cryptoquant.api.okex.setting import api_key, seceret_key, passphrase
    symbol = 'OKB-USDT'
    minutes = '5m'  #     策略交易周期，K线支持，15分钟，30分钟，1小时，1天
    trading_volume = 1  # 单笔交易量
    spotapi = OkexSpotV3(api_key, seceret_key, passphrase,True)

    # 获取 TICK
    tick_data = spotapi.spot_ticker(symbol)
    print(tick_data)
    
    # 获取K线
    spot_kline = spotapi.spot_kline(symbol,minutes)
    print(spot_kline)

    # 计算交易信号
    # 判断是否买入
    order_price = 2
    size = 1
    order_type = 'limit'
    side = 'buy'

    data = spotapi.spot_order(symbol,order_price, size, order_type, side)
    print(data)

    while True:
        pass
        # 1 获取数据

        # 2 处理数据，计算交易信号

        # 3 根据信号，买卖



