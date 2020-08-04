# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         MaStrategy
# Description:  Binance strategy
# Author:       Rudy
# U:            project
# Date:         2020-04-20
#-------------------------------------------------------------------------------

"""
StudyQuant:项目制的量化投资学院，帮你快速入行量化交易。
wechat:82789754
"""

# from cryptoquant.api.binance_gateway.SQbinanceclient import BinanceRestApi
# from binance_f.model.constant import OrderSide,OrderType,TradeDirection,CandlestickInterval
import time
from cryptoquant.event.engine import Event, EventEngine,EVENT_TIMER
import numpy as np
import talib
from cryptoquant.trader.constant import (
    Direction,
    OrderType,
    Interval,
    Exchange,
    Offset,
    Status)
from cryptoquant.app.strategies.StrategyTemplate import CtaTemplate
from cryptoquant.app.strategies.engine import CtaEngine
import traceback
from cryptoquant.trader.event import EVENT_TICK,EVENT_TRADE,EVENT_ORDER,EVENT_POSITION,EVENT_KLINE,EVENT_OPEN_ORDER,EVENT_LOG,\
EVENT_ACCOUNT,EVENT_CONTRACT
# from vnpy.trader.object import OrderRequest

from cryptoquant.trader.ArrayManager import ArrayManager, current_minute, scheduleTime, crossover, \
    crossunder
from cryptoquant.trader.object import TickData, BarData, TradeData, OrderData
from cryptoquant.trader.utility import BarGenerator, ArrayManager



class SQMA_strategy(CtaTemplate):
    # 策略参数
    symbol = 'EOSUSDT'
    Exchange = Exchange.BINANCE

    #pos = 0
    order_volume = 1
    run_time = 0                # 策略时间
    size = 10                   # 深度行情挡位
    atrWindow = 20              # ATR 参数
    total_pos = 0
    pos = {}                    # 仓位
    order_type = 'limit'        # 下单类型
    slMultiplier = 2.1          # 移动止损参数
    # minute = CandlestickInterval.MIN1 # K线周期
    short_ma_windows = 10        # 短均线参数
    long_ma_windows = 20        # 长均线参数


    # log = createLog() # 日志

    def __init__(self, cta_engine,strategy_name, vt_symbol, setting):
        """
        初始化策略
        :param cta_engine:
        :param strategy_name:
        :param vt_symbol:
        :param setting:
        """
        super().__init__(cta_engine,strategy_name, vt_symbol, setting)
        self.symbol = vt_symbol
        self.cta_engine = cta_engine
        self.vt_symbol = vt_symbol
        if setting:
            self.minutes = setting['minutes']

        self.bg = BarGenerator(self.on_bar)
        self.am = ArrayManager()

        # 创建K线合成器对象
        self.bg5 = BarGenerator(self.on_bar, 5, self.on5MinBar)
        self.am5 = ArrayManager()
        print('当前运行时间:%s'%time.strftime("%Y-%m-%d %X", time.localtime()))
        print('初始化成功')

    def register_event(self):
        self.cta_engine.event_engine.register(EVENT_POSITION, self.on_pos)
        self.cta_engine.event_engine.register(EVENT_KLINE, self.on_kline)
        self.cta_engine.event_engine.register(EVENT_OPEN_ORDER, self.on_open_orders)
        self.cta_engine.event_engine.register(EVENT_TICK, self.on_tick)
        self.cta_engine.event_engine.register(EVENT_TIMER, self.on_timer)

    def on_pos(self, event: Event):
        pass

    def on_init(self):
        """
        Callback when strategy is inited.
        """
        self.write_log("策略初始化")
        self.load_bar(1)

    def on_tick(self, tick: TickData):
        """
        Callback of new tick data update.
        """
        self.bg.update_tick(tick)
        print(tick)
        # self.trading = True

    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """
        self.handle_bar(bar)
        self.bg5.update_bar(bar)
        # self.bg15.update_bar(bar)

    def handle_bar(self,bar:BarData):
        """
        策略逻辑函数
        """
        am = self.am
        am.update_bar(bar)
        if not am.inited:
            return

        fast_ma = am.sma(self.short_ma_windows, array=True)
        self.fast_ma0 = fast_ma[-1]
        self.fast_ma1 = fast_ma[-2]

        slow_ma = am.sma(self.long_ma_windows, array=True)
        self.slow_ma0 = slow_ma[-1]
        self.slow_ma1 = slow_ma[-2]

        cross_over = self.fast_ma0 > self.slow_ma0 and self.fast_ma1 < self.slow_ma1
        cross_below = self.fast_ma0 < self.slow_ma0 and self.fast_ma1 > self.slow_ma1

        if cross_over:
            if self.pos == 0:
                self.buy(bar.close_price, 1)
            elif self.pos < 0:
                self.cover(bar.close_price, 1)
                self.buy(bar.close_price, 1)

        elif cross_below:
            if self.pos == 0:
                self.short(bar.close_price, 1)
            elif self.pos > 0:
                self.sell(bar.close_price, 1)
                self.short(bar.close_price, 1)

        self.put_event()

    def on5MinBar(self,bar:BarData):
        """5分钟K线调用"""
        print(bar)

    def on_kline(self, data):
        try:
            #得到K线
            self.kline = data[self.symbol]
            # self.kline = self.get_kline(symbol,minute)
            close = np.array(self.kline['close'])
            # upper, middle, lower = talib.BBANDS(close, timeperiod=self.bollWindow, nbdevup=self.bollDev, nbdevdn=self.bollDev, matype=0)
            short_ma = talib.MA(close, self.short_ma_windows)
            long_ma = talib.MA(close, self.long_ma_windows)
            #计算交易信号
            if crossover(short_ma, long_ma):  # 如果向上突破上轨
                signal = 1
            elif crossunder(long_ma, short_ma):  # 如果向下突破下轨
                signal = -1
            else:
                signal = 0

            # 获取持仓
            data = self.get_position(self.symbol)
            self.pos = data['positionAmt']  # 获取持仓数量

            # 当前无仓位，发送开仓委托
            if self.pos == 0:
                ticker = self.kline.iloc[-1]  # run.ticker(symbol)
                # print(ticker)
                self.intraTradeHigh = ticker['high']
                self.intraTradeLow = ticker['low']
                self.enterprice = ticker['close']

                if signal == 1:
                    print('买入')
                    current_price = self.get_ticker(self.symbol)['price']
                    self.buy(current_price, 1) # 参数： 价格，交易量
                if signal == -1:
                    current_price = self.get_ticker(self.symbol)['price']
                    self.short(current_price, 1)

            # 持有多头仓位
            elif self.pos > 0:
                if signal == -1:
                    current_price = self.get_ticker(self.symbol)['price']
                    data = self.short(current_price, 1)
                    print(data)

            # 持有空头仓位：
            elif self.pos < 0:
                if signal == 1:
                    current_price = self.get_ticker(self.symbol)['price']
                    self.buy(current_price, 1)

            self.minutes_report()
        except Exception as e:
            self.on_error(e)
            traceback.print_exc()
        pass


    def on_error(self,e):
        print(e)

    def on_open_orders(self, event: Event):
        self.buy(1,1)
        pass

    def on_timer(self, event: Event):
        pass

    def on_timer(self, event: Event):
        pass

    def get_position(self,symbol = None):
        """调用获取持仓方法"""
        return self.cta_engine.gateway.get_position(symbol)

    def get_kline(self,symbol,minutes):
        """获取当前价格"""
        return self.cta_engine.gateway.get_kline(symbol,minutes)

    def get_ticker(self,symbol):
        """获取当前价格"""
        return self.cta_engine.gateway.get_ticker(symbol)

    def handle_data(self,symbol,minute):
        pass

    def minutes_report(self, close=None):
        """策略回调日志"""
        info = {}
        info['symbol'] = self.symbol
        info['strategy_cycle'] = self.minutes
        info['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        info['pos'] = self.pos

        # info['short_positon'] = self.short_position
        # info['trader_number'] = self.trader_number
        if close != None:
            info['close'] = self.current_price

        print(info)
        # self.log.info(info)

    def write_log(self, msg: str):
        """
        Write a log message.
        """
        self.cta_engine.write_log(msg, self)


"""
好好学习，天天向上。 
project
"""