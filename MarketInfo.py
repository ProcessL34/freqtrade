import urllib.parse
import datetime

import requests
import pandas as pd
from okx import MarketData


class MarketInfo:
    def __init__(self):
        self.sorted_usdt_tickers = None
        apikey = "60898b23-6437-40d0-b257-042249b83db5"
        secretkey = "D4AC49DE52C069DFA1362C785D687923"
        passphrase = 'Liucheng_34'
        self.url = 'https://aws.okx.com'
        self.MarketApi = MarketData.MarketAPI(apikey, secretkey, passphrase,
                                              use_server_time=False, flag='0', domain=self.url)
        self.sort_tickers()

    def get_sorted_tickers(self):
        return self.sorted_usdt_tickers

    def sort_tickers(self):
        tickers = pd.DataFrame((self.MarketApi.get_tickers('SWAP'))['data'])
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
        response = self.MarketApi.get_history_candlesticks(instId, bar=bar, limit=limit)
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
    # history_candles = market_info.get_history_candles('BTC-USDT-SWAP', '1D', '60')
    # sorted_tickers = market_info.get_sorted_tickers()
    # print(sorted_tickers.head(10)['growth_rate'].iloc[0])
    # print(type(sorted_tickers.head(10)['growth_rate'].iloc[0]))
