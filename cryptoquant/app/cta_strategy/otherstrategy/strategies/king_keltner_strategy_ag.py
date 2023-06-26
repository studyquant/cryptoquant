import time

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
from strategy_factors.kc import king_keltner
from collections import defaultdict
from sq_strategy.SqStrategyTemplate import SqStrategy_Template,TargetPosTemplate
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

from cryptoquant.app.datamodel.constant import (
    Product,
    OrderStatus,
    Runmode,
    Direction
)

from cryptoquant import Interval, SymbolType, OrderType, RunMode
from cryptoquant.api.api_gateway.pro.apigateway_v8 import  ApiGateway

class KingKeltnerStrategy(CtaTemplate,SqStrategy_Template):
    """"""

    author = "AgileQuant"
    skew = 0                        # 下单时候偏离程度
    kk_length = 20                  # KK 均线参数
    kk_dev = 2                      # KK dev参数
    # trailing_percent = 0.8
    # fixed_size = 1
    long_etf_symbol = "TQQQ"        # 做多的标的
    short_etf_symbol = "SQQQ"       # 做空的标的
    long_order_amount = 1           # 做多的 数量
    short_order_amount = 1          # 做空的数量
    short_etf_pos = 0               # 空头ETF的持仓数量
    long_etf_pos = 0                # 空头ETF的持仓数量
    order_amount = 1                # 固定下单量参数
    kk_up = 0
    kk_down = 0
    intra_trade_high = 0
    intra_trade_low = 0
    target_pos_map = defaultdict(list)
    long_vt_orderids = []
    short_vt_orderids = []
    vt_orderids = []
    strategy_symbol_list = []
    # 策略symbol 列表
    parameters = ["kk_length", "kk_dev", "trailing_percent", "fixed_size"]
    variables = ["kk_up", "kk_down"]

    def __init__(self, cta_engine:ApiGateway, strategy_name, vt_symbol, setting):
        """"""
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        self.exchange = cta_engine
        for key, value in setting.items():
            self.__dict__[key] = value
        # K线生成器
        self.bg = BarGenerator(self.on_bar, 15, self.on_5min_bar)
        # 计算指标的一个容器对象
        self.am = ArrayManager()
        self.init_target_pos_strategy(cta_engine, strategy_name, vt_symbol, setting)

    def on_init(self):
        """
        Callback when strategy is inited.
        """
        self.write_log("策略初始化")
        self.load_bar(10)
    def init_target_pos_strategy(self,cta_engine, strategy_name, vt_symbol, setting):
        """
        初始化目标仓位管理系统
        """
        self.strategy_symbol_list.append(self.long_etf_symbol)
        self.strategy_symbol_list.append(self.short_etf_symbol)
        self.strategy_symbol_list.append(vt_symbol)
        for symbol in self.strategy_symbol_list:
            self.target_pos_map[symbol] = TargetPosTemplate(cta_engine, strategy_name, vt_symbol, setting)

    def on_start(self):
        """
        Callback when strategy is started.
        """
        self.write_log("策略启动")

    def on_stop(self):
        """
        Callback when strategy is stopped.
        """
        self.write_log("策略停止")

    def on_tick(self, tick: TickData):
        """
        Callback of new tick data update.
        """
        self.bg.update_tick(tick)

    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """
        self.bg.update_bar(bar)

        if hasattr(self,'kc'):
            self.process_pos(bar)

    def process_pos(self,bar):
        if self.pos > 0:
            if bar.close_price < self.kc.mid.to_list()[-1]:
                self.sell(bar.close_price,abs(self.pos))
                signal = '多头回归中线'
                print('{}: 当前仓位：{} ,信号：{}, sell{}'.format(bar.datetime, self.pos, signal, self.pos))
        elif self.pos < 0:
            if bar.close_price > self.kc.mid.to_list()[-1]:
                self.cover(bar.close_price, abs(self.pos))
                signal = '空头回归中线'
                print('{}: 当前仓位：{} ,信号：{}, buy{}'.format(bar.datetime, self.pos, signal, self.pos))
    def on_5min_bar(self, bar: BarData):
        """"""
        self.bar = bar
        if self.trading == False:
            return
        else:
            pass
        for orderid in self.vt_orderids:
            self.cancel_order(orderid)
        self.vt_orderids.clear()

        am = self.am
        am.update_bar(bar)
        if not am.inited:
            return

        self.handle_data()

    def on_kline(self,kline_df):
        """
        实盘交易调用K线函数
        :param kline_df:
        :return:
        """
        self.write_log('on_kline: get kline data sucessfully ')
        am = self.am
        am.close_array = kline_df['close'].to_list()
        am.high_array = kline_df['high'].to_list()
        am.low_array = kline_df['low'].to_list()
        am.open_array = kline_df['open'].to_list()
        am.volume_array = kline_df['volume'].to_list()
        self.handle_data()


    def on_position(self,position:Position):
        """期货交易"""
        if position != []:
            msg = f"on_position: symbol: {position.symbol}  持仓:{position.Amount} , strategy_pos: {self.pos}, {position.symbol}成本价:{position.cost_basis}, market_price:{position.last_sale_price}"
            self.write_log(msg)
            if position.symbol == self.long_etf_symbol:
                self.long_etf_pos = position.Amount
            elif position.symbol == self.short_etf_symbol:
                self.short_etf_pos = position.Amount
            else:
                pass
        else:
            msg = f" 持仓为空 ： {position}"
            # msg = f"on_position: symbol: {position.symbol}  " \
            #       f"持仓:{position.Amount} ," \
            #       f" strategy_pos: {self.pos}, " \
            #       f"{position.symbol}成本价:{position.cost_basis}, " \
            #       f"market_price:{position.last_sale_price}"
            self.write_log(msg)



        # position = Position()
        # position.update_tiger(position_data)
        # # print(pos.__dict__)
        # if self.symbol in position.symbol:
        #     self.pos = position.amount
        #     self.position = position.__dict__
        #     msg = f"on_position:  pos: {self.pos }, {position.symbol} : Amount:{position.Amount} , 成本价:{position.cost_basis}, market_price:{position.last_sale_price}"
        #     self.write_log(msg)

    def on_order(self,order):
        # print(order)
        if self.mode== RunMode.LIVE:
            msg = f" {order.Info.contract.symbol} : {order.__str__()}"
            self.write_log(msg)

    def get_ticker(self,symbol):
        if self.market_permission:
            ticker = self.exchange.GetTicker(symbol=symbol)
        else:
            ticker = self.exchange.GetDelayTicker(symbol=symbol)
        return ticker



    def calculate_order_amount(self,ticker, account,direction):
        """

        返回 下单数量
        """
        self.total_balance = account.Available_balance
        self.available_balance = self.order_amount_pct * self.total_balance * self.leverage
        self.able_buy_amount = int(self.available_balance / ticker.Sell)
        self.able_sell_amount = int(self.available_balance / ticker.Buy)  # 计算可卖量
        order_amount = self.able_buy_amount if direction == Direction.LONG else  self.able_sell_amount
        msg = f"账户总余额 {self.total_balance} ， 可用余额： {self.available_balance}  可买量： {self.able_buy_amount}， 可卖量： {self.able_sell_amount } " \
              f"下单量 ： {order_amount}  卖价：{ticker.Sell}， 买价：{ticker.Buy}"
        self.write_log(msg)
        return order_amount

    def get_order_price_and_amount(self,symbol,  order_amount = None, direction = None):
        """
        获取价格和下单数量
        order_amount = None, 则赋值为 1
        """
        ticker = self.exchange.get_us_ticker(symbol)
        # self.write_log(ticker.__str__())
        order_price = ticker.Sell if direction == Direction.LONG else ticker.Buy

        if not order_amount:
            account= self.account_info
            # 计算买卖量
            order_amount = self.calculate_order_amount(ticker,account,Direction.LONG)


        return order_price, order_amount


    def update_target_pos_manager_position(self,symbol):
        target_pos_manager = self.target_pos_map.get(symbol)
        target_pos_manager.update_position()


    def strategy_buy(self,symbol, order_amount =None):
        """
        策略如何买的逻辑
        """
        # 如果没有下单数量,计算可买数量
        order_price, order_amount = self.get_order_price_and_amount(symbol,order_amount=order_amount, direction=Direction.LONG)

        # 设置目标仓位
        # target_pos_manager = self.target_pos_map.get(symbol)
        # target_pos_manager.set_target_pos(order_amount)
        buy_order = self.exchange.order(symbol , order_price, order_amount, direction=Direction.LONG)
        # time.sleep(2)
    def strategy_short(self,symbol,order_amount =None):
        """
        策略如何买的逻辑
        """
        order_price, order_amount = self.get_order_price_and_amount(symbol,order_amount=order_amount, direction=Direction.SHORT)
        sell_order = self.exchange.order(symbol , order_price, order_amount, direction=Direction.SHORT)
        time.sleep(2)

    def on_tick_and_kline(self,ticker, kline):
        """
        tick 实盘的逻辑函数
        """
        if not hasattr(self, 'bar'):
            self.bar = self.am.bar_data

        self.kc = king_keltner(kline=kline)
        self.kc.up, self.kc.mid, self.kc.down = self.kc.keltner(self.kk_length, self.kk_dev, array=True)                    # 计算指标
        mid = self.kc.mid.to_list()[-1]
        signal = self.kc.get_ticker_signal(ticker)
        mid_price = (ticker.Buy + ticker.Sell)/2
        msg = f"Ticker _ 非多即空信号： {signal} current_mid_price : {mid_price}, 时间周期：{self.time_frame} ,  均价: {mid}"
        self.write_log(msg)
        self.on_signal(signal)

    def on_tick_and_kline2(self, ticker, kline):
        """
        tick 实盘的逻辑函数 , 现货，只买TQ
        """
        if not hasattr(self, 'bar'):
            self.bar = self.am.bar_data

        self.kc = king_keltner(kline=kline)
        self.kc.up, self.kc.mid, self.kc.down = self.kc.keltner(self.kk_length, self.kk_dev, array=True)  # 计算指标
        mid = self.kc.mid.to_list()[-1]
        signal = self.kc.get_ticker_signal(ticker)
        mid_price = (ticker.Buy + ticker.Sell) / 2
        msg = f"Ticker非多即空信号： {signal} current_mid_price : {mid_price}, 时间周期：{self.time_frame}, 均价:{mid}"
        self.write_log(msg)
        self.spot_strategy(signal)

    def handle_data(self):
        """期货交易"""
        # 获取日线
        df = self.am.get_dataframe()
        self.kc = king_keltner(kline=df) # 实例对象
        # 计算KC 指标
        self.kc.keltner(self.kk_length, self.kk_dev, array=True)  # 计算指标

        if not hasattr(self, 'bar'):
            self.bar = self.am.bar_data
        # 获取日线的KC 信号
        signal = self.kc.king_keltner_signal(self.kk_length, self.kk_dev)
        self.write_log( f"策略金叉/死叉 信号 {signal}")
        self.on_signal(signal)

    def on_signal(self,signal):
        """
        信号处理逻辑
        """
        # signal = -1
        self.write_log(f'on_strategy_signal:{signal}')
        # 回测逻辑
        if self.mode == RunMode.BACKTESTING:
            if self.pos == 0:
                # 回测的逻辑
                self.process_us_stock_signal(signal, self.bar)
            elif self.pos != 0:
                hold_signal = self.kc.get_simple_hold_position_signal(pos=self.pos, n=11, kk_dev=2)
                # print(hold_signal)
                self.process_us_stock_signal(hold_signal, self.bar)

        # 实盘逻辑
        else:
            # signal = -1
            if self.long_etf_pos == 0 and self.short_etf_pos == 0:
                if signal == 1:
                    self.strategy_buy(symbol=self.long_etf_symbol)
                elif signal == -1:
                    self.strategy_buy(symbol=self.short_etf_symbol)
                else:
                    pass
            # 处理多头ETF交易信号
            self.process_long_etf_position(signal)
            # 处理空头ETF交易信号
            self.process_short_etf_position(signal)

        self.put_event()

    def spot_strategy(self,signal):
        """
        现货交易策略
        新的策略其实和现在这个没有太大的区别 唯一的区别就是他不会两头买 只会做多
        """
        # signal =1
        if self.long_etf_pos == 0:
            if signal == 1:
                # self.strategy_buy(symbol = self.long_etf_symbol)
                self.strategy_buy(symbol=self.long_etf_symbol, order_amount=self.order_amount)
            else:
                pass

        # 处理多头ETF交易信号
        self.process_long_etf_position(signal)

    def process_long_etf_position(self,signal):
        # 持有多头的的多头ETF，（持有多头）
        if self.long_etf_pos != 0 :
            self.write_log(f"process_long_etf_position :long_etf_pos: {self.long_etf_pos} ")

        pos = abs(self.long_etf_pos)

        if self.long_etf_pos >0:
            if signal == -1:
                self.write_log(f"short_long_etf, process_long_etf_position :long_etf_pos: {self.long_etf_pos}, signal:{signal} ")
                self.strategy_short(symbol = self.long_etf_symbol,order_amount=pos)

        # 持有空头的的多头ETF，（持有空头）
        elif self.long_etf_pos <0:
            if signal == 1:
                self.write_log(f"buy_long_etf, process_long_etf_position :long_etf_pos: {self.long_etf_pos}, signal:{signal} ")
                self.strategy_buy(symbol = self.long_etf_symbol,order_amount=pos)

            else:
                # 其实不应该持有任何 空头的 TQ
                self.write_log(
                    f"process_long_etf_position : 平错误仓位 -> buy TQQQ {pos} ,  long_etf_pos: {self.long_etf_pos}, signal:{signal} ")
                self.strategy_buy(symbol=self.long_etf_symbol, order_amount=pos)

        else:
            pass


    def process_short_etf_position(self,signal):
        # 持有空头的负持仓（持有空头）
        pos = abs(self.short_etf_pos)
        if self.short_etf_pos != 0 :
            self.write_log(f"process_short_etf_position :short_etf_pos: {self.short_etf_pos} ")

        if self.short_etf_pos >0:
            if signal == 1:
                self.write_log(f"short_short_etf, process_short_etf_position : short_etf_pos: {self.short_etf_pos}, signal:{signal} ")
                self.strategy_short(symbol=self.short_etf_symbol, order_amount=pos)

        # 持有空头的负持仓（持有多头）
        elif self.short_etf_pos <0:
            if signal == -1: # 做空
                self.write_log(f"buy_short_etf, process_short_etf_position : short_etf_pos:  {self.short_etf_pos}, signal:{signal} ")
                self.strategy_buy(symbol=self.short_etf_symbol, order_amount=pos)
            else:
                # 其实不应该持有任何 空头的 TQ
                self.write_log(
                    f"process_short_etf_position : 平错误仓位 -> buy SQQQ {pos} ,  short_etf_symbol: {self.short_etf_symbol}, signal:{signal} ")
                self.strategy_buy(symbol=self.short_etf_symbol, order_amount=pos)

        else:

            pass

    def on_trade(self, trade: TradeData):
        """
        Callback of new trade data update.
        """
        if self.pos != 0:
            if self.pos > 0:
                for short_orderid in self.short_vt_orderids:
                    self.cancel_order(short_orderid)

            elif self.pos < 0:
                for buy_orderid in self.long_vt_orderids:
                    self.cancel_order(buy_orderid)

            for orderid in self.long_vt_orderids + self.short_vt_orderids:
                if orderid in self.vt_orderids:
                    self.vt_orderids.remove(orderid)

        self.put_event()

    def send_oco_order(self, buy_price, short_price, volume):
        """"""
        self.long_vt_orderids = self.buy(buy_price, volume, True)
        self.short_vt_orderids = self.short(short_price, volume, True)

        self.vt_orderids.extend(self.long_vt_orderids)
        self.vt_orderids.extend(self.short_vt_orderids)

    def on_stop_order(self, stop_order: StopOrder):
        """
        Callback of stop order update.
        """
        pass
