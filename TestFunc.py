# import requests
#
# # CryptoCompare API的基本URL
# base_url = 'https://min-api.cryptocompare.com/data/'
#
#
# # 获取比特币的市值排名信息
# def get_bitcoin_market_info():
#     url = base_url + 'top/mktcapfull?limit=10&tsym=USD'
#     response = requests.get(url)
#     data = response.json()
#     return data
#
#
# if __name__ == '__main__':
#     # 调用函数并打印结果
#     bitcoin_info = get_bitcoin_market_info()
#     print(bitcoin_info)

import requests


def get_crypto_rank(crypto_name):
    # 发送GET请求获取特定加密货币的市值排名
    response = requests.get(f'https://api.coingecko.com/api/v3/coins/{crypto_name}')

    # 将响应转换为JSON格式
    data = response.json()

    # 获取加密货币的市值排名
    if 'market_cap_rank' in data:
        crypto_rank = data['market_cap_rank']
        print(f"The rank of {crypto_name} is {crypto_rank}")
        return crypto_rank
    else:
        print(f"Market cap rank data not available for {crypto_name}")
        return -1


if __name__ == '__main__':
    get_crypto_rank('bitcoin')
