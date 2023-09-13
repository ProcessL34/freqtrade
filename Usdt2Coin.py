from okx.PublicData import PublicAPI

api_key = '-1'
secret_key = '-1'
passphrase = '-1'
domain = 'https://aws.okx.com'
public_api = PublicAPI(api_key, secret_key, passphrase, flag='0', domain=domain)

# 获取转换的交易对信息
result = public_api.get_convert_contract_coin(type='1', instId='BTC-USDT-SWAP', sz='5', px='30000', unit='usdt')
print(result)

