#! python3

import time, re
import logging, os
import bs4, sys
from selenium import webdriver

logging.disable(logging.CRITICAL)

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
log = logging.getLogger(__name__)


class vipurl:
    def __init__(self, args, tool_url):
        # log.info('video url: ' + url)
        self.args = args
        self.tool_url = tool_url
        self.address = {}
        self.path = 'D:/Tools/watchvip_caches'
        self.filename = os.path.join(self.path, 'url_temp.txt')
        self.title = ''
        self.browser = None
        self.source = ''
        self.soup = None

    def backup(self):
        # 备份videoUrl
        os.makedirs(self.path, exist_ok=True)
        temp = open(self.filename, 'a+')
        localtime = time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
        temp.write('{} -- {} {}\n'.format(localtime, self.title, self.args.url[0]))
        temp.close()

    def previous_url(self):
        with open(self.filename, 'r') as f:
            lines = f.readlines()
            n = len(lines)
            while True:
                self.args.url[0] = re.search('http.*', lines[n-1]).group()
                if self.args.url[0][0:4] == 'http':
                    break
                n = n -1

    def open_browser(self):
            # 打开浏览器
            #SERVICE_ARGS = ['--load-images=false']  # 禁止加载图片
            #self.browser = webdriver.Chrome(service_args=SERVICE_ARGS)
            chrome_options = webdriver.ChromeOptions()
            #chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('log-level=3')
            chrome_options.add_argument('user-data-dir=C:/Users/MaSiyuan/AppData/Local/Google/Chrome/User Data')
            self.browser = webdriver.Chrome(chrome_options=chrome_options)
            self.browser.implicitly_wait(5)
            self.browser.get(self.args.url[0].strip())
            self.source = self.browser.page_source
            self.soup = bs4.BeautifulSoup(self.source, 'lxml')  # 解析HTML

    def show_log(self):
        os.system('cat {}'.format(self.filename))
        sys.exit()

    def get_title(self):
        i = 0
        while True:
            if self.soup.title.text[i] == '第':    # for qq
                break
            if self.soup.title.text[i] == '_':    # for iqiyi
                break
            if i >= len(self.soup.title.text):
                break
            self.title += self.soup.title.text[i]
            i += 1
        print('剧名：{}'.format(self.title.strip()))

    def __tencentVip(self):
        """查找腾讯VIP电视剧剧集网址"""
        if self.args.is_all:
            for a in self.soup.select("span a[href^='/x/cover']"):
                span = a.find_parent('span')
                if span.find(name='img', attrs={'alt': '预告'}):
                    continue
                num = a.text.strip()[0:2]
                href = a.get('href')
                href = self.tool_url + 'https://v.qq.com' + href  # 得到最终网址
                self.address[num] = href
            return

        for img in self.soup.select("span img[alt='vip']"):  # 查找span标签下属性alt='vip'的img子标签
            span = img.find_parent('span')  # 返回img标签的父标签span
            num = span.find(name='a').text.strip()[0:2]  # 获得a标签的文本，即集数
            href = span.find(name='a').get('href')  # 再查找span标签下a标签，并获得属性href
            href = self.tool_url + 'https://v.qq.com' + href  # 得到最终网址
            self.address[num] = href

    def __iqiyiVip(self):
        """查找爱奇艺VIP电视剧剧集网址"""
        if self.args.is_all:
            for a in self.soup.select("li[class='album_item'] a"):
                if a.select("i[class*='new']"):
                    continue
                num = a.text.strip()
                if len(num) > 2:
                    continue
                href = a.get('href')
                if href.startswith('java'):
                    continue
                href = self.tool_url + href  # 得到最终网址
                self.address[num] = href
            return

        for span in self.soup.select("li i[class*='vip']"):
            li = span.find_parent('li')
            num = li.find(name='a').text.strip()
            if len(num) > 2:
                continue
            href = li.find('a').get('href')
            href = self.tool_url + href
            self.address[num] = href

    def __youkuVip(self):
        """查找优酷VIP电视剧剧集网址"""
        if self.args.is_all:
            for a in self.soup.select("div a"):
                num = a.text.strip()[0:2]
                href = a.get('href')
                href = self.tool_url + 'https:' + href  # 得到最终网址
                self.address[num] = href

        for span in self.soup.select("div a span[class*='vip']"):
            div = span.find_parent('div')
            num = div.text.strip()[0:2]
            a = div.find(name='a')
            href = a.get('href')
            href = self.tool_url + 'https:' + href
            self.address[num] = href

    def __sohuVip(self):
        """查找搜狐VIP电视剧剧集网址"""
        for em in self.soup.select("li a em[class*='vip']"):
            li = em.find_parent('li')
            num = li.text.strip()
            a = li.find(name='a')
            href = a.get('href')
            href = self.tool_url + 'https:' + href
            self.address[num] = href

    def get_address(self):
        if 'v.qq.com' in self.args.url[0]:
            self.__tencentVip()
        elif 'iqiyi.com' in self.args.url[0]:
            self.__iqiyiVip()
        elif 'v.youku.com' in self.args.url[0]:
            self.__youkuVip()
        elif 'tv.sohu.com' in self.args.url[0]:
            self.__sohuVip()

    def play(self):
        if self.args.is_list:
            self.show_log()
        if self.args.is_prev:
            self.previous_url()

        self.open_browser()
        self.get_title()
        self.backup()
        self.get_address()

        print('The following videos can be played: ')
        for key, value in self.address.items():
            print(key + ' -- ' + value)

        while True:
            num = input('\nPlease Enter order number of video(q to quit): ')
            if num == 'q':
                self.browser.close()
                sys.exit()
            if num not in self.address.keys():
                print('The order number no exists!')
                continue
            try:
                self.browser.get(self.address[num])  # 打开播放网页，VIP，不存在的！
                print('#' + num + ' is being played...')
            except Exception as exc:
                print(exc)