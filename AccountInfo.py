from Constants import RUN_LOG
from Logger import Logger
from okx import Account

log = Logger(RUN_LOG).logger


class AccountInfo:
    def __init__(self):
        # 创建一个日志记录器
        self.url = 'https://aws.okx.com'
        api_key = "a6306a4a-2687-4405-ae02-5bc6e5f2a2b1"
        api_secret_key = "366CC4C3D54F3F5954A523A38144AD6D"
        passphrase = 'Liucheng_34'
        self.account_api = Account.AccountAPI(api_key, api_secret_key, passphrase, flag='0',
                                              domain=self.url)

    def is_invested(self, invest_id):
        self.account_api.get_positions(instType=invest_id)

