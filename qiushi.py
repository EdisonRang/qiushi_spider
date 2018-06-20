import requests

class QiuShi(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
        }
        self.base_url = 'https://www.qiushibaike.com/'
        self.file = open('qiushi.json', 'w')


