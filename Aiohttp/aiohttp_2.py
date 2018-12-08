#! python3
# _*_ coding: utf-8 _*_
"""
@Project: Aiohttp
@Author: masiyuan
@Time: 2018/12/7 22:40
"""
'''
同步方式爬取当当畅销书的图书信息
'''

import time
import requests
import pandas as pd
from lxml import etree
from bs4 import BeautifulSoup

# table表格用于储存书本信息
table = []

# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}

# 处理网页
def download(url):
    res = requests.get(url, headers=headers)
    res.encoding = 'gbk'

    # 利用BeautifulSoup将获取到的文本解析成HTML
    soup = BeautifulSoup(res.text, "lxml")
    # 获取网页中的畅销书信息
    book_list = soup.find(name='ul', class_='bang_list clearfix bang_list_mode')('li')
    for book in book_list:
        info = book.find_all('div')
        # 获取每本畅销书的排名，名称，评论数，作者，出版社
        rank = info[0].text[0:-1]
        name = info[2].text
        comments = info[3].text.split('条')[0]
        author = info[4].text
        date_and_publisher = info[5].text.split()
        publisher = date_and_publisher[1] if len(date_and_publisher) >= 2 else ''

        # 将每本畅销书的上述信息加入到table中
        table.append([rank, name, comments, author, publisher])


# 全部网页
urls = ['http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-recent7-0-0-1-%d' % i for i in range(1, 26)]

# 统计该爬虫的消耗时间
print('#' * 50)
t1 = time.time()  # 开始时间

for url in urls:
    download(url)

# 将table转化为pandas中的DataFrame并保存为CSV格式的文件
df = pd.DataFrame(table, columns=['rank', 'name', 'comments', 'author', 'publisher'])
df.to_csv('dangdang.csv', index=False)

t2 = time.time()  # 结束时间
print('使用一般方法，总共耗时：%s' % (t2 - t1))
print('#' * 50)
