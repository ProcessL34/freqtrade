import requests
import pandas as pd
import plotly.graph_objects as go

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
    print(tickers)
    return tickers


def get_coin_growth(tickers, inst_id):
    growth_rate = tickers.loc[tickers['instId'] == inst_id, 'growth_rate'].values[0]
    print('btc growth rate', growth_rate)
    return growth_rate


sorted_tickers = get_sorted_tickers()

btc_growth_rate = get_coin_growth(sorted_tickers, 'BTC-USDT-SWAP')


historical = pd.DataFrame((requests.get(url + '/api/v5/market/history-candles?instId=BTC-USDT-SWAP').json())['data'])
# print(historical)
historical.columns = ["Date", "Open", "High", "Low", "Close", "Vol", "volCcy", "volCcyQuote", "confirm"]
historical['Date'] = pd.to_datetime(historical['Date'], unit='ms')
historical.set_index('Date', inplace=True)
historical.sort_values(by='Date')
# print(historical)
historical['20 SMA'] = historical.Close.rolling(20).mean()
historical.tail()

fig = go.Figure(data=[go.Candlestick(x=historical.index,
                                     open=historical['Open'],
                                     high=historical['High'],
                                     low=historical['Low'],
                                     close=historical['Close'],
                                     ),
                      go.Scatter(x=historical.index, y=historical['20 SMA'], line=dict(color='purple', width=1))])

# fig.show()

trades = requests.get(url + '/api/v5/market/trades?instId=BTC-USDT').json()
var = trades['data']
# print(var)
