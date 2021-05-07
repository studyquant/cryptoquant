# encoding: UTF-8

"""
导入JQDATA数据至VNPY
"""
from cryptoquant.trader.constant import Direction, Exchange, Interval, Offset, Status, Product, OptionType, OrderType
import pandas as pd
# from cryptoquant.app.data_manage.data_manager import save_data_to_cryptoquant
from cryptoquant.trader.constant import Direction, Exchange, Interval, Offset, Status, Product, OptionType, OrderType
from cryptoquant.trader.database import database_manager
# import jqdatasdk
from datetime import datetime
from cryptoquant.trader.object import BarData

def save_data_to_cryptoquant(symbol, df,exchange):
    """
    将数据导入VNPY数据库
    :param symbol:  存入的标的名
    :param df: 数据
    :param exchange: 交易所名字
    :return:
    """

    # symbol = symbol + '.'+exchange.name
    # symbol = 'IF88'
    print(symbol)
    bars = []
    count = 0
    start = False
    for index, row in df.iterrows():
        # print(row)
        dt = datetime.strptime(row['Date'] + ' ' + row['Time'], '%Y-%m-%d %H:%M:%S')

        bar = BarData(
            symbol=symbol,
            exchange=exchange,
            datetime=dt,
            interval=Interval.MINUTE,
            volume=row['TotalVolume'],
            open_price=row['Open'],
            high_price=row['High'],
            low_price=row['Low'],
            close_price=row['Close'],
            gateway_name="DB",
        )
        bars.append(bar)
        # do some statistics
        count += 1
        if not start:
            start = bar.datetime

    end = bar.datetime
    database_manager.save_bar_data(bars)
    print("插入数据", start, "-", end, "总数量：", count)


if __name__ == '__main__':
    df = pd.read_csv('IF9999.csv')
    symbol = 'IF9999'
    save_data_to_cryptoquant(symbol, df, Exchange.CFFEX)

    # data = pd.read_csv('dataMerged_XBTUSD_2017-01-01_to_2020-04-26.csv')
    # #数据清洗
    # df = pd.DataFrame()
    # df['Open'] = data['open']
    # df['Close'] = data['close']
    # df['Low'] = data['low']
    # df['High'] = data['high']
    # df['TotalVolume'] = data['volume']
    # df['Date'] =  [date[:10] for date in data['date']]
    # df['Time'] =  [date[11:19] for date in data['date']]
    #
    # symbol = 'XBTUSD'
    # studyquant_save_data_to_vnpy(symbol, df, Exchange.BITMEX)



