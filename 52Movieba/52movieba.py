#! python3

import sys
from pyquery import PyQuery
from selenium import webdriver
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}

class Movieba:
    def __init__(self, url):
        self.url = url
        self.source = ''

    def get_one_page(self, num):
        try:
            url = self.url + str(num) + '.htm'
            res = requests.get(url, headers=headers)
            self.source = res.text
        except Exception as exc:
            print(exc)
            sys.exit()

    def parse_one_page(self):
        doc = PyQuery(self.source)
        ls_a = doc("td[class*='td-subject'] a[target='_blank']").items()
        for a in ls_a:
            text = a.text()
            if text.startswith('[公告]'):
                continue
            index = text.index(']')
            print(text[(index+1):])

    def run(self):
        while (True):
            num = input('请输入网页页码(1-84)(q to quit): ')
            if num == 'q':
                return
            self.get_one_page(num)
            self.parse_one_page()

if __name__ == '__main__':
    url = 'http://www.52movieba.com/forum/index-'
    m = Movieba(url)
    m.run()