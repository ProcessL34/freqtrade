import Constants
from Logger import Logger
from PwdLoader import PwdLoader
from PwdObserver import PwdObserver
from okx import Account

log = Logger.get_logger(Constants.RUN_LOG)


class AccountInfo(PwdObserver):
    def __init__(self):
        PwdLoader.add_subscriber(self)
        account_key = PwdLoader.load_pwd_static()
        self.account_api = Account.AccountAPI(account_key['apikey'],
                                              account_key['secretkey'],
                                              account_key['passphrase'],
                                              flag='0',
                                              domain=account_key['url'])

    def update(self, account_key):
        self.account_api = Account.AccountAPI(account_key['apikey'],
                                              account_key['secretkey'],
                                              account_key['passphrase'],
                                              flag='0',
                                              domain=account_key['url'])

    # 获取订单信息
    def get_positions_info(self, invest_id):
        return self.account_api.get_positions(instType=invest_id)

    def is_invested(self, invest_id):
        return True

    def has_handled(self, invest_id):
        return True

    def can_invest(self, invest_id):
        return True


if __name__ == '__main__':
    account_info = AccountInfo()
    log.info(account_info.get_positions_info(''))
