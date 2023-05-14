import requests
import pandas as pd
import plotly.graph_objects as go
from okx.Trade import TradeAPI

url = 'https://aws.okx.com'

tickers = pd.DataFrame((requests.get(url + '/api/v5/market/tickers?instType=SWAP').json())['data'])
tickers = tickers.drop('instType', axis=1)
print(len(tickers))
# print(tickers.tail().T)

ticker = requests.get(url + '/api/v5/market/ticker?instId=BTC-USD-SWAP').json()
# print(ticker)

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



