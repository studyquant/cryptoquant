"""
=========================================================
* author: rudy
* email: 
=========================================================
"""

import pandas as pd
import numpy as np
from datetime import datetime
from functools import wraps

def tryit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # print('Calling decorated function')
        try:
            # print(f'args:{args}')
            # print(f'kwargs:{kwargs}')
            result = func(*args, **kwargs)
            # print(f'函数返回结果 {result}')
            return result
        except Exception as err:
            print(err)
            return err
    return wrapper


def timeit(func):
    """
    统计花了多少时间
    :param func:
    :return:
    """


    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        # print(f'args:{args}')
        # print(f'kwargs:{kwargs}')
        result = func(*args, **kwargs)
        print(f'一共花费了{datetime.now() - start_time} 秒')
        # print(f'函数返回结果 {result}')
        return result
    return wrapper


@timeit
@tryit
def example(a,k=2,b=3):
     """Docstring"""
     print('Called example function', a)
     result = 2+2
     return result


if __name__ == "__main__":
    example(5)
    pass
