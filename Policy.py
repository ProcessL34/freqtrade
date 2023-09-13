# 创建 OKEx API 客户端
from okx import Trade
from okx import PublicData
import math
from plotly.io import json
import requests

from MarketInfo import MarketInfo
from Constants import *
import json

class Policy:
    def __init__(self, base_inv):
        self.url = 'https://aws.okx.com'
        apikey = "60898b23-6437-40d0-b257-042249b83db5"
        secretkey = "D4AC49DE52C069DFA1362C785D687923"
        passphrase = 'Liucheng_34'
        self.trade = Trade.TradeAPI(apikey, secretkey, passphrase, False, '0')  # Limit Order
        self.market_info = MarketInfo()
        self.publicDataApi = PublicData.PublicAPI(apikey, secretkey, passphrase, use_server_time=False, flag='0', domain=self.url)
        self.public_data = self.publicDataApi.get_instruments("SWAP")
        self.base_inv = base_inv

    def get_ct_value_price(self, ins_id, price):
        if self.public_data['code'] == SUCCESS_CODE:
            for item in self.public_data['data']:
                if item['instId'] == ins_id:
                    return float(item['ctVal'])*float(price)
        else:
            return float('inf')

    def core_investment(self):
        sorted_tickers = self.market_info.get_sorted_tickers()
        btc_growth_rate = self.market_info.get_coin_growth(BTC_USDT_SWAP)
        for index, row in sorted_tickers.iterrows():
            if (btc_growth_rate > 0.03 and row['growth_rate'] > 0.5) or (
                    btc_growth_rate < 0.01 and row['growth_rate'] > 0.05):
                min_inv = self.get_ct_value_price(row[INST_ID], row[BID_PX])
                self.trade.place_order(instId=row[INST_ID], tdMode='cross', side='sell',
                                       ordType='limit', sz=math.floor(self.base_inv/min_inv), px=row['bidPx'])


if __name__ == '__main__':
    policy = Policy(5)
    policy.core_investment()


