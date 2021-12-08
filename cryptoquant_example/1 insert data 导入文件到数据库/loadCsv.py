# encoding: UTF-8

"""
导入JQDATA数据至VNPY
"""
from cryptoquant.trader.constant import Direction, Exchange, Interval, Offset, Status, Product, OptionType, OrderType
from cryptoquant.trader.database import database_manager
import pandas as pd
from cryptoquant.app.data_manage.data_manager import studyquant_save_data_to_cryptoquant

if __name__ == '__main__':
    df = pd.read_csv('IF9999.csv')
    symbol = 'IF9999'
    studyquant_save_data_to_cryptoquant(symbol, df, Exchange.CFFEX)

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



