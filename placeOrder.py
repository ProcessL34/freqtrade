# 创建 OKEx API 客户端
from okx.Trade import TradeAPI
from plotly.io import json
import requests

url = 'https://aws.okx.com'

apikey = "e38df133-643d-4f66-bc0e-beb0844f3d9c"
secretkey = "9BDB88B186EC078E8FA69A066D515E28"
passphrase = 'Liucheng_34'

client = TradeAPI(apikey, secretkey, passphrase, False, '0')  # Limit Order

# print(result)
print(client.place_order(instId='UMA-USDT-SWAP', tdMode='cross', side='sell',
                         ordType='limit', sz='3', px='3.26'))