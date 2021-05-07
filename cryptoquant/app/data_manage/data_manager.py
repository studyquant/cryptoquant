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



if __name__=="__main__":
    pass
    
    
    
    
    
    
    
"""
好好学习，天天向上。 
project
"""