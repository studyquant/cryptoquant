# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         data_manager.py
# Description:  
# Author:       Rudy
# U:            project
# Date:         2020-03-30
#-------------------------------------------------------------------------------

"""
StudyQuant:项目制的量化投资学院，帮你快速入行量化交易。
wechat:82789754
"""
from cryptoquant.trader.constant import Direction, Exchange, Interval, Offset, Status, Product, OptionType, OrderType
from cryptoquant.trader.database import database_manager
# import jqdatasdk
from datetime import datetime
from cryptoquant.trader.object import BarData


def studyquant_save_data_to_vnpy(symbol, df,exchange):
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

def studyquant_get_data_from_jqdata(symbol, start_date, end_date,frequency):
    """
    :return:
    """
    data1 = jqdatasdk.get_price(symbol, start_date=start_date, end_date=end_date, frequency=frequency)  # 获得000001.XSHG的2015年12月1号14:00-2015年12月2日12:00的分钟数据
    print(data1.head())
    data1 = data1.dropna()
    data1['index1'] = data1.index
    data1['Date'] = data1['index1'].map(lambda x: str(x)[0:10])
    data1['Time'] = data1['index1'].map(lambda x: str(x)[11:])
    data1['volume'] = data1['volume'].map(lambda x: int(x))
    data2 = data1[['Date', 'Time', 'open', 'high', 'low', 'close', 'volume']]
    data2.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'TotalVolume']
    print('下载完成')
    return data2


if __name__=="__main__":
    pass
    
    
    
    
    
    
    
"""
好好学习，天天向上。 
project
"""