import json
import time

import schedule as schedule

from Constants import RUN_LOG
from Logger import Logger

log = Logger.get_logger(Constants.RUN_LOG)


class PwdLoader:
    subscribers = []
    pwd = None

    def __init__(self):
        self.pwd = None
        self.load_pwd_static()

    def load_pwd(self):
        log.info("周期性任务执行")
        # 打开JSON文件
        with open('resources/pwd.json', 'r') as file:
            # 读取JSON数据
            self.pwd = json.load(file)
        for subscriber in PwdLoader.subscribers:
            subscriber.update(self.pwd)

    @staticmethod
    def add_subscriber(subscriber):
        PwdLoader.subscribers.append(subscriber)

    @staticmethod
    def load_pwd_static():
        if PwdLoader.pwd is None:
            with open('resources/pwd.json', 'r') as file:
                PwdLoader.pwd = json.load(file)
        return PwdLoader.pwd

    # 定义一个周期性执行的任务函数
    def init_loader_task(self):
        interval = 5
        schedule.every(interval).seconds.do(self.load_pwd)
        while True:
            schedule.run_pending()
            time.sleep(interval)

    def notify_events(self):
        for subscribe in self.subscribers:
            subscribe.update(self.pwd)


if __name__ == '__main__':
    loader = PwdLoader()
    loader.init_loader_task()
