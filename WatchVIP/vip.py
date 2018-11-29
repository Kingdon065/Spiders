#! python3

import logging
import bs4, requests, sys
from selenium import webdriver

logging.disable(logging.CRITICAL)

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
log = logging.getLogger(__name__)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}

class vipurl:
    def __init__(self, args, tool_url):
        # log.info('video url: ' + url)
        self.__args = args
        self.__tool_url = tool_url
        self.__address = {}
        try:
            #SERVICE_ARGS = ['--load-images=false']  # 禁止加载图片
            #self.__browser = webdriver.Chrome(service_args=SERVICE_ARGS)
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--ignore-certificate-errors')
            self.__browser = webdriver.Chrome(chrome_options=chrome_options)
            self.__browser.implicitly_wait(5)
            self.__browser.get(self.__args.root.strip())
            self.__source = self.__browser.page_source
            self.__soup = bs4.BeautifulSoup(self.__source, 'lxml')  # 解析HTML
        except Exception as exc:
            log.error(exc)
            sys.exit()

    def title(self):
        i = 0
        title = ''
        while True:
            if self.__soup.title.text[i] == '第':    # for qq
                break
            if self.__soup.title.text[i] == '_':    # for iqiyi
                break
            if i >= len(self.__soup.title.text):
                break
            title += self.__soup.title.text[i]
            i += 1
        print('剧名：{}'.format(title.strip()))

    def __tencentVip(self):
        """查找腾讯VIP电视剧剧集网址"""
        if self.__args.is_all:
            for a in self.__soup.select("span a[href^='/x/cover']"):
                span = a.find_parent('span')
                if span.find(name='img', attrs={'alt': '预告'}):
                    continue
                num = a.text.strip()[0:2]
                href = a.get('href')
                href = self.__tool_url + 'https://v.qq.com' + href  # 得到最终网址
                self.__address[num] = href
            return

        for img in self.__soup.select("span img[alt='vip']"):  # 查找span标签下属性alt='vip'的img子标签
            span = img.find_parent('span')  # 返回img标签的父标签span
            num = span.find(name='a').text.strip()[0:2]  # 获得a标签的文本，即集数
            href = span.find(name='a').get('href')  # 再查找span标签下a标签，并获得属性href
            href = self.__tool_url + 'https://v.qq.com' + href  # 得到最终网址
            self.__address[num] = href

    def __iqiyiVip(self):
        """查找爱奇艺VIP电视剧剧集网址"""
        if self.__args.is_all:
            for a in self.__soup.select("li[class='album_item'] a"):
                if a.select("i[class*='new']"):
                    continue
                num = a.text.strip()
                if len(num) > 2:
                    continue
                href = a.get('href')
                if href.startswith('java'):
                    continue
                href = self.__tool_url + href  # 得到最终网址
                self.__address[num] = href
            return

        for span in self.__soup.select("li i[class*='vip']"):
            li = span.find_parent('li')
            num = li.find(name='a').text.strip()
            if len(num) > 2:
                continue
            href = li.find('a').get('href')
            href = self.__tool_url + href
            self.__address[num] = href

    def __youkuVip(self):
        """查找优酷VIP电视剧剧集网址"""
        if self.__args.is_all:
            for a in self.__soup.select("div a"):
                num = a.text.strip()[0:2]
                href = a.get('href')
                href = self.__tool_url + 'https:' + href  # 得到最终网址
                self.__address[num] = href

        for span in self.__soup.select("div a span[class*='vip']"):
            div = span.find_parent('div')
            num = div.text.strip()[0:2]
            a = div.find(name='a')
            href = a.get('href')
            href = self.__tool_url + 'https:' + href
            self.__address[num] = href

    def __sohuVip(self):
        """查找搜狐VIP电视剧剧集网址"""
        for em in self.__soup.select("li a em[class*='vip']"):
            li = em.find_parent('li')
            num = li.text.strip()
            a = li.find(name='a')
            href = a.get('href')
            href = self.__tool_url + 'https:' + href
            self.__address[num] = href

    def get_address(self):
        if 'v.qq.com' in self.__args.root:
            self.__tencentVip()
        elif 'iqiyi.com' in self.__args.root:
            self.__iqiyiVip()
        elif 'v.youku.com' in self.__args.root:
            self.__youkuVip()
        elif 'tv.sohu.com' in self.__args.root:
            self.__sohuVip()

    def play(self):
        print('The following videos can be played: ')
        for key, value in self.__address.items():
            print(key + ' -- ' + value)

        while True:
            num = input('\nPlease Enter order number of video(q to quit): ')
            if num == 'q':
                self.__browser.close()
                sys.exit()
            if num not in self.__address.keys():
                print('The order number no exists!')
                continue
            try:
                self.__browser.get(self.__address[num])  # 打开播放网页，VIP，不存在的！
                print('#' + num + ' is being played...')
            except Exception as exc:
                print(exc)