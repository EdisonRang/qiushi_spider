import json
from queue import Queue
from lxml import etree
import requests
import threading

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
        # 构建三个数据队列
        self.url_queue = Queue()
        self.res_queue = Queue()
        self.data_queue = Queue()

    def generate_url_list(self):
        # self.url_list = [self.base_url.format(i) for i in range(1,14)]
        for i in range(1,14):
            url = self.base_url.format(i)
            self.url_queue.put(url)

    def get(self):
        while True:
            url = self.url_queue.get()
            print('正在获取{}对应的响应'.format(url))
            response = requests.get(url, headers= self.headers)
            # 判断响应状态
            if response.status_code == 503:
                self.url_queue.put(url)
            else:
                self.res_queue.put(response.content)
            self.url_queue.task_done()

    def parse(self):
        while True:
            data = self.res_queue.get()
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
            self.data_queue.put(data_list)
            self.res_queue.task_done()

    def save(self):
        while True:
            data_list = self.data_queue.get()
            print('正在保存数据')
            for data in data_list:
                str_data = json.dumps(data) + ',\n'
                self.file.write(str_data)
            self.data_queue.task_done()

    def run(self):
        # # 构建url_list
        # self.generate_url_list()
        # # 遍历url
        # for url in self.url_list:
        #     # 发起请求
        #     data = self.get(url)
        #     # 解析请求
        #     data_list = self.parse(data)
        #     # 保存数据
        #     self.save(data_list)
        # 创建多线程列表
        threading_list = []
        # 创建生成url列表的线程
        t_generate_url = threading.Thread(target=self.generate_url_list)
        threading_list.append(t_generate_url)
        # 创建发送请求的线程
        for i in range(4):
            t_get = threading.Thread(target=self.get)
            threading_list.append(t_get)
        # 创建解析出具的线程
        for i in range(3):
            t_parse = threading.Thread(target=self.parse)
            threading_list.append(t_parse)
        # 创建保存数据的线程
        t_save = threading.Thread(target=self.save)
        threading_list.append(t_save)
        # 设置线程并开启线程
        for t in threading_list:
            # 设置守护线程
            t.setDaemon(True)
            t.start()

        # 设置主线程等待
        for q in [self.url_queue, self.res_queue, self.data_queue]:
            q.join()

if __name__ == '__main__':
    qiushi = QiuShi()
    qiushi.run()

