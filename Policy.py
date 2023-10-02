# 创建 OKEx API 客户端

from Constants import *
from Logger import Logger
from MarketInfo import MarketInfo
from okx import PublicData, Account
from okx import Trade

log = Logger(RUN_LOG).logger


class Policy:
    def __init__(self, base_inv):
        # 创建一个日志记录器

        self.url = 'https://aws.okx.com'
        api_key = "a6306a4a-2687-4405-ae02-5bc6e5f2a2b1"
        api_secret_key = "366CC4C3D54F3F5954A523A38144AD6D"
        passphrase = 'Liucheng_34'
        self.trade = Trade.TradeAPI(api_key, api_secret_key, passphrase, False, '0')  # Limit Order
        self.market_info = MarketInfo()
        self.publicDataApi = PublicData.PublicAPI(api_key, api_secret_key, passphrase, flag='0',
                                                  domain=self.url)
        self.public_data = self.publicDataApi.get_instruments("SWAP")
        self.base_inv = base_inv

        self.account_api = Account.AccountAPI(api_key, api_secret_key, passphrase, flag='0',
                                              domain=self.url)

    def get_ct_value_price(self, ins_id, price):
        if self.public_data['code'] == SUCCESS_CODE:
            for item in self.public_data['data']:
                if item['instId'] == ins_id:
                    return float(item['ctVal']) * float(price)
        else:
            return float('inf')

    def core_investment(self):
        sorted_tickers = self.market_info.get_sorted_tickers()
        btc_growth_rate = self.market_info.get_coin_growth(BTC_USDT_SWAP)
        for index, row in sorted_tickers.iterrows():
            if (btc_growth_rate > 0.03 and row['growth_rate'] > 0.5) or (
                    btc_growth_rate < 0.01 and row['growth_rate'] > 0.1):
                min_inv = self.get_ct_value_price(row[INST_ID], row[BID_PX])
                # self.trade.place_order(instId=row[INST_ID], tdMode='cross', side='sell',
                # ordType='limit', sz=math.floor(self.base_inv / min_inv), px=row['bidPx'])


if __name__ == '__main__':
    policy = Policy(5)
    policy.core_investment()
    balance = policy.account_api.get_account_balance()
    positions = policy.account_api.get_positions()
    log.info(balance)
