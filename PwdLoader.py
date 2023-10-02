import json


class PwdLoader:
    def __init__(self):
        pwd = self.load_pwd()
        self.api_key = pwd['apikey']
        self.secret_key = pwd['secretkey']

    def load_pwd(self):
        # 打开JSON文件
        with open('resources/pwd.json', 'r') as file:
            # 读取JSON数据
            return json.load(file)

    def get_api_key(self):
        return self.api_key

    def get_secret_key(self):
        return self.secret_key


if __name__ == '__main__':
    loader = PwdLoader()
    print(loader.get_secret_key())
    print(loader.get_api_key())