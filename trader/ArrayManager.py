# encoding: UTF-8
import numpy as np
import talib
from datetime import datetime, timedelta
import pandas as pd


def crossover(a, b):
    """向上突破"""
    if a[-2] < b[-2] and a[-1] > b[-1]:
        return True
    else:
        return False
    
def crossunder(a, b):
    """向下突破"""
    if a[-2] > b[-2] and a[-1] < b[-1]:
        return True
    else:
        return False


def current_minute(minutes):
    minutes = int(minutes.strip('m'))
    now_time = datetime.now().minute
    if now_time % minutes == 0:
        return now_time
    else:
        now_time -= now_time % minutes
        return now_time
        
def scheduleTime(minutes,plus_minute = 1):
    '''更新时间'''
    minute = int(minutes.strip('m'))
    total_time = []
    inited_time = datetime(2019, 1, 1, 00, 00, 00, 0)
    for i in range(int(24 * 60/minute)):
        inited_time +=  timedelta(minutes = minute) 
        newtime = inited_time + timedelta(minutes = plus_minute) 
        total_time.append(newtime)
        
    total_time = pd.to_datetime(total_time)
    schedule_time = []
    for time2 in total_time:
        target_time = str(time2)[-8:-3]
#            print (target_time)
        schedule_time.append(target_time)
    return schedule_time





########################################################################
class ArrayManager(object):
    """
    K线序列管理工具，负责：
    1. K线时间序列的维护
    2. 常用技术指标的计算
    """

    # ----------------------------------------------------------------------
    def __init__(self, size=150):
        """Constructor"""
        self.count = 0  # 缓存计数
        self.size = size  # 缓存大小
        self.inited = False  # True if count>=size

        self.openArray = np.zeros(size)  # OHLC
        self.highArray = np.zeros(size)
        self.lowArray = np.zeros(size)
        self.closeArray = np.zeros(size)
        self.volumeArray = np.zeros(size)

    def updateBar(self, bar):
        """更新K线"""
        self.count += 1
        if not self.inited and self.count >= self.size:
            self.inited = True

        self.openArray[:-1] = self.openArray[1:]
        self.highArray[:-1] = self.highArray[1:]
        self.lowArray[:-1] = self.lowArray[1:]
        self.closeArray[:-1] = self.closeArray[1:]
        self.volumeArray[:-1] = self.volumeArray[1:]

        self.openArray[-1] = bar.open
        self.highArray[-1] = bar.high
        self.lowArray[-1] = bar.low
        self.closeArray[-1] = bar.close
        self.volumeArray[-1] = bar.volume

    def updatekline(self, kline):
        """更新K线"""
        self.openArray = kline.open
        self.highArray = kline.high
        self.lowArray = kline.low
        self.closeArray = kline.close
        self.volumeArray = kline.volume

    # ----------------------------------------------------------------------
    @property
    def open(self):
        """获取开盘价序列"""
        return self.openArray

    # ----------------------------------------------------------------------
    @property
    def high(self):
        """获取最高价序列"""
        return self.highArray

    # ----------------------------------------------------------------------
    @property
    def low(self):
        """获取最低价序列"""
        return self.lowArray

    # ----------------------------------------------------------------------
    @property
    def close(self):
        """获取收盘价序列"""
        return self.closeArray

    # ----------------------------------------------------------------------
    @property
    def volume(self):
        """获取成交量序列"""
        return self.volumeArray

    # ----------------------------------------------------------------------
    def sma(self, n, array=False):
        """简单均线"""
        result = talib.SMA(self.close, n)
        if array:
            return result
        return result[-1]

    # ----------------------------------------------------------------------
    def std(self, n, array=False):
        """标准差"""
        result = talib.STDDEV(self.close, n)
        if array:
            return result
        return result[-1]

    # ----------------------------------------------------------------------
    def cci(self, n, array=False):
        """CCI指标"""
        result = talib.CCI(self.high, self.low, self.close, n)
        if array:
            return result
        return result[-1]

    # ----------------------------------------------------------------------
    def atr(self, n, array=False):
        """ATR指标"""
        result = talib.ATR(self.high, self.low, self.close, n)
        if array:
            return result
        return result[-1]

    # ----------------------------------------------------------------------
    def rsi(self, n, array=False):
        """RSI指标"""
        result = talib.RSI(self.close, n)
        if array:
            return result
        return result[-1]

    # ----------------------------------------------------------------------
    def macd(self, fastPeriod, slowPeriod, signalPeriod, array=False):
        """MACD指标"""
        macd, signal, hist = talib.MACD(self.close, fastPeriod,
                                        slowPeriod, signalPeriod)
        if array:
            return macd, signal, hist
        return macd[-1], signal[-1], hist[-1]

    # ----------------------------------------------------------------------
    def adx(self, n, array=False):
        """ADX指标"""
        result = talib.ADX(self.high, self.low, self.close, n)
        if array:
            return result
        return result[-1]

    # ----------------------------------------------------------------------
    def boll2(self, n, k, array=False):
        """ADX指标"""
        upper, middle, lower = talib.BBANDS(self.close, timeperiod=n, nbdevup=k, nbdevdn=k, matype=0)
        #    print(upper, middle, lower)
        if array:
            return upper, middle, lower
        return upper[-1], middle[-1], lower[-1]

    # ----------------------------------------------------------------------
    def boll(self, n, dev, array=False):
        """布林通道"""
        mid = self.sma(n, array)
        std = self.std(n, array)

        up = mid + std * dev
        down = mid - std * dev

        return up, down

        # ----------------------------------------------------------------------

    def keltner(self, n, dev, array=False):
        """肯特纳通道"""
        mid = self.sma(n, array)
        atr = self.atr(n, array)

        up = mid + atr * dev
        down = mid - atr * dev

        return up, down

    # ----------------------------------------------------------------------
    def donchian(self, n, array=False):
        """唐奇安通道"""
        up = talib.MAX(self.high, n)
        down = talib.MIN(self.low, n)

        if array:
            return up, down
        return up[-1], down[-1]



    # ----------------------------------------------------------------------
    @staticmethod
    def MACD_signal(MACD2):
        """MACD 信号"""
        buy_signal = 0
        if MACD2[-2] < 0 and MACD2[-1] > 0:
            buy_signal = 1
        elif MACD2[-2] > 0 and MACD2[-1] < 0:
            buy_signal = -1
        else:
            buy_signal = 0
        return buy_signal

    # ----------------------------------------------------------------------
    def MACD_diff(position, hist, close):
        '''
        a:记录所有MACD交叉点
        i:索引最近出现的交叉点
        '''
        record_result = []
        for i in range(len(hist)):
            # 金叉
            if i >= 2:
                if hist[:i + 1][-2] < 0 and hist[:i + 1][-1] > 0:
                    result = True
                    record_result.append(result)
                # 死叉
                elif hist[:i + 1][-2] > 0 and hist[:i + 1][-1] < 0:
                    result = False
                    record_result.append(result)
                else:
                    record_result.append(hist[i])
            else:
                record_result.append(hist[i])

        a = pd.Series(record_result)
        checkT = a[a == True]
        checkF = a[a == False]
        last_true = checkT.index[-position]
        last_false = checkF.index[-position]
        #    print (last_false,'last False')
        #    print (last_true,'last True')

        # 计算上一个死叉的MACD总和：
        if last_true > last_false:
            final = hist[last_false:last_true]
            print ('死叉转金叉 ： 死叉的面积')
            gold_macd = True

        else:
            final = hist[last_true:last_false]
            print ('金叉转死叉 ： 金叉的面积')
            gold_macd = False

        if len(final) == 0:
            print('转折点太近，面积为一个数')
            final = hist[last_true:last_false]
            lowest_close = min(close[last_true:last_false])  # 区间最小值
            largest_close = max(close[last_true:last_false])  # 区间最小值
        else:
            if gold_macd:
                lowest_close = min(close[last_false:last_true])  # 区间最小值
                largest_close = max(close[last_false:last_true])  # 区间最小值

            elif gold_macd == False:
                lowest_close = min(close[last_true:last_false])  # 区间最小值
                largest_close = max(close[last_true:last_false])  # 区间最小值

        total = sum(final)
        print('total:%s' % (total))
        # print('final',final)
        #    print('lowest_close', lowest_close)
        #    print('largest_close',largest_close)
        return total, largest_close, lowest_close
