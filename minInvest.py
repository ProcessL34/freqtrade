import requests
import json
import time
import datetime

url = "https://aws.okx.com/api/v5/tradingBot/grid/min-investment"
now = datetime.datetime.utcnow()
timestamp = int(time.mktime(now.timetuple()))

headers = {
    "Content-Type": "application/json",
    'OK-ACCESS-KEY': "e38df133-643d-4f66-bc0e-beb0844f3d9c",
    'OK-ACCESS-SIGN': '9BDB88B186EC078E8FA69A066D515E28',
    'OK-ACCESS-TIMESTAMP': str(timestamp)
}

data = {
    "instType": "CSPR-USDT-SWAP"
}

response = requests.post(url, headers=headers, data=json.dumps(data))
response_json = response.json()

print(response_json)
# min_investment = response_json['investmentData'][0]['amt']

# print(f"CSPR-USDT-SWAP最小投资数为：{min_investment}")
