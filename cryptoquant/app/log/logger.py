"""
web:  studyquant.com
author: Rudy
wechat:82789754
"""
import logging

class StrategyLogger(logging.Logger):
    def __init__(self, name,
                 file=None,
                 level="INFO",
                 fmt="%(asctime)s| %(name)s | %(message)s",
                 datefmt="%Y-%m-%d %H:%M:%S"):
        super().__init__(name, level)

        self.fmt = fmt
        self.formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)
        if file:
            self.logger = logging.getLogger(file)
            self.file_handler = logging.FileHandler(filename=file, encoding="utf-8")
            self.file_handler.setLevel(level)
            self.file_handler.setFormatter(self.formatter)
            self.addHandler(self.file_handler)

            console = logging.StreamHandler()
            console.setLevel(logging.INFO)
            console.setFormatter(self.fmt)  # 添加CONSOLE 的打印格式
            self.addHandler(console)
            self.logger.addHandler(self.file_handler)
            self.logger.addHandler(console)

        # return self.logger


import time
import os


def log_engine(name):
    # current_path = os.getcwd()
    # path = os.path.join(current_path, name + '.txt')
    # if os.path.exists(path):
    #     mode = 'a'
    # else:
    #     mode = 'w'

    # logging.basicConfig(
    #     level=logging.INFO,
    #     format='%(asctime)s %(filename)s %(lineno)d %(levelname)s %(message)s',
    #     filename=path,
    #     filemode=mode
    # )

    logger = logging.getLogger(name)
    logger.setLevel(level=logging.INFO)

    rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    current_path = os.getcwd()
    path = os.path.join(current_path, 'log')
    # log_path = os.path.dirname(os.getcwd()) + '/logs/'
    log_name = path + rq + '.txt'

    handler = logging.FileHandler(log_name)
    handler.setLevel(logging.INFO)

    logger.addHandler(handler)

    # 设置格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    # logger.addHandler(handler)
    # 写在文件中
    # logger.info("Start print log")
    # logger.debug("Do something")
    # logger.warning("Something maybe fail.")
    # logger.info("Finish")
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)  # 添加CONSOLE 的打印格式
    logger.addHandler(console)
    # logger.info("Start print log")
    # logger.info("Start print log")
    return logger


class LogEngine():

    def __init__(self, name):
        self.log = log_engine(name)

    def info(self, message=None):
        self.log.info(message)


if __name__ == "__main__":
    pass
    # logger = StrategyLogger('test2','test.log')
    # text=
    # logger2 = log_engine(';test')
    # logger2 = StrategyLogger('name')
    # logger2.warning('okex | test')
    log = LogEngine('start')
    log.info('start')

    log.info('start')
