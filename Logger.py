import logging
from logging import handlers

import Constants

LOG_LEVEL = logging.INFO


class Logger:
    def __init__(self, log_name):
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(LOG_LEVEL)  # 设置日志级别
        format_str = logging.Formatter('%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        screen_handler = logging.StreamHandler()  # 往屏幕上输出
        screen_handler.setFormatter(format_str)  # 设置屏幕上显示的格式
        file_handler = handlers.RotatingFileHandler(filename=log_name, maxBytes=100000, backupCount=10,
                                                    encoding='utf-8')
        file_handler.setFormatter(format_str)

        self.logger.addHandler(screen_handler)
        self.logger.addHandler(file_handler)


if __name__ == '__main__':
    log = Logger(Constants.TRADE_LOG)
    log.logger.debug('debug')
    log.logger.info('info')
    log.logger.warning('警告')
    log.logger.error('报错')
    log.logger.critical('严重')
    log2 = Logger(Constants.RUN_LOG)
    log2.logger.info('liucheng')
