import urllib.parse
import datetime

import requests
import pandas as pd

url = 'https://aws.okx.com'


def get_sorted_tickers():
    tickers = pd.DataFrame((requests.get(url + '/api/v5/market/tickers?instType=SWAP').json())['data'])
    print(len(tickers))
    # print(tickers.tail())
    tickers['sodUtc8'] = tickers['sodUtc8'].astype(float)
    tickers['last'] = tickers['last'].astype(float)
    tickers['growth_rate'] = (tickers['last'] - tickers['sodUtc8']) / tickers['sodUtc8']
    tickers['growth_rate'] = tickers['growth_rate'].apply(lambda x: '{:.3%}'.format(x))
    tickers = tickers.sort_values(by=['growth_rate'], ascending=False)
    print(tickers.head(10))
    return tickers


def get_history_candles():
    # 构造请求参数
    params = {
        'instId': 'BTC-USDT-SWAP',
        'bar': '1D',
        'limit': '60'
    }
    query_string = urllib.parse.urlencode(params)
    response = requests.get(f"{url}/api/v5/market/history-candles?{query_string}")
    print(response)
    historical = pd.DataFrame((response.json())['data'])
    print(historical)
    return historical


def get_coin_growth(tickers, inst_id):
    growth_rate = tickers.loc[tickers['instId'] == inst_id, 'growth_rate'].values[0]
    print('btc growth rate', growth_rate)
    return growth_rate


sorted_tickers = get_sorted_tickers()

btc_growth_rate = get_coin_growth(sorted_tickers, 'BTC-USDT-SWAP')

history_candles = get_history_candles()
