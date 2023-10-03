import logging
from logging import handlers

import Constants

LOG_LEVEL = logging.INFO


class Logger:
    LoggersMap = {}

    @staticmethod
    def get_logger(log_name):
        if log_name in Logger.LoggersMap:
            return Logger.LoggersMap[log_name].logger
        else:
            logger_instance = Logger(log_name)
            Logger.LoggersMap[log_name] = logger_instance
            return logger_instance.logger

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
    logger = Logger.get_logger(Constants.RUN_LOG)
    logger.info("liucheng")
    logger.error("liucheng")
    logger2 = Logger.get_logger(Constants.RUN_LOG)
    logger2.info("liucheng")
    logger2.error("liucheng")