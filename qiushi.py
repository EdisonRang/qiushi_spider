import json

from lxml import etree
import requests

class QiuShi(object):
    """
    爬取糗事百科信息爬虫
    """
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
        }
        self.base_url = 'https://www.qiushibaike.com/8hr/page/{}/'
        self.url_list = None
        self.file = open('qiushi.json', 'w')

    def generate_url_list(self):
        self.url_list = [self.base_url.format(i) for i in range(1,14)]

    def get(self, url):
        print('正在获取{}对应的响应'.format(url))
        response = requests.get(url, headers= self.headers)
        return response.content

    def parse(self, data):
        print('正在解析响应')
        # 构建element对象
        html = etree.HTML(data)
        # 获取所有帖子节点列表
        node_list = html.xpath('//*[@id="content-left"]/div')
        data_list = []
        for node in node_list:
            temp = {}
            try:
                temp['user'] = node.xpath('./div/a[2]/h2/text()')[0]
                temp['link'] = 'https://www.qiushibaike.com' + node.xpath('./div/a[2]/@href')[0]
                temp['age'] = node.xpath('./div/div/text()')[0]
                temp['gender'] = node.xpath('./div/div/@class')[0].split(" ")[1].split("I")[0]
            except:
                temp['user'] = '匿名用户'
                temp['link'] = None
                temp['age'] = None
                temp['gender'] = None
            temp['content'] = node.xpath('./a/div/span[1]/text()')
            data_list.append(temp)
        return data_list

    def save(self, data_list):
        print('正在保存数据')
        for data in data_list:
            str_data = json.dumps(data) + ',\n'
            self.file.write(str_data)

    def run(self):
        # 构建url_list
        self.generate_url_list()
        # 遍历url
        for url in self.url_list:
            # 发起请求
            data = self.get(url)
            # 解析请求
            data_list = self.parse(data)
            # 保存数据
            self.save(data_list)

if __name__ == '__main__':
    qiushi = QiuShi()
    qiushi.run()

