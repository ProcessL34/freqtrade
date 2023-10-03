import pandas as pd

from Constants import RUN_LOG
from Logger import Logger
from PwdLoader import PwdLoader
from PwdObserver import PwdObserver
from okx import MarketData

log = Logger.get_logger(Constants.RUN_LOG)


class MarketInfo(PwdObserver):
    def __init__(self):
        PwdLoader.add_subscriber(self)
        self.market_api = None
        self.sorted_usdt_tickers = None
        self.url = 'https://aws.okx.com'
        account_key = PwdLoader.load_pwd_static()
        self.market_api = MarketData.MarketAPI(account_key['apikey'],
                                               account_key['secretkey'],
                                               account_key['passphrase'],
                                               flag='0',
                                               domain=account_key['url'])
        self.sort_tickers()

    def update(self, account_key):
        self.market_api = MarketData.MarketAPI(account_key['apikey'],
                                               account_key['secretkey'],
                                               account_key['passphrase'],
                                               flag='0',
                                               domain=account_key['url'])
        self.sort_tickers()

    def get_sorted_tickers(self):
        return self.sorted_usdt_tickers

    def sort_tickers(self):
        tickers = pd.DataFrame((self.market_api.get_tickers('SWAP'))['data'])
        usdt_tickers = tickers[tickers['instId'].str.contains('USDT')]
        print(usdt_tickers.info())

        print('usdt_tickers length: ', len(usdt_tickers))
        usdt_tickers['sodUtc8'] = usdt_tickers['sodUtc8'].astype(float)
        usdt_tickers['last'] = usdt_tickers['last'].astype(float)
        usdt_tickers['growth_rate'] = (usdt_tickers['last'] - usdt_tickers['sodUtc8']) / usdt_tickers['sodUtc8']
        usdt_tickers = usdt_tickers.sort_values(by=['growth_rate'], ascending=False)
        print('usdt_tickers.head: \n', usdt_tickers.head(5))
        self.sorted_usdt_tickers = usdt_tickers

    def get_history_candles(self, instId, bar, limit):
        response = self.market_api.get_history_candlesticks(instId, bar=bar, limit=limit)
        historical = pd.DataFrame(response['data'])
        return historical

    def get_coin_growth(self, inst_id):
        growth_rate = self.sorted_usdt_tickers.loc[self.sorted_usdt_tickers['instId'] == inst_id, 'growth_rate'].values[
            0]
        return growth_rate


if __name__ == '__main__':
    market_info = MarketInfo()
    market_info.sort_tickers()
    btc_growth_rate = market_info.get_coin_growth('BTC-USDT-SWAP')
    log.info(btc_growth_rate)
    # history_candles = market_info.get_history_candles('BTC-USDT-SWAP', '1D', '60')
    # sorted_tickers = market_info.get_sorted_tickers()
    # print(sorted_tickers.head(10)['growth_rate'].iloc[0])
    # print(type(sorted_tickers.head(10)['growth_rate'].iloc[0]))
