#! python3

import requests
import csv
from bs4 import BeautifulSoup


url = 'http://maoyan.com/board/4?offset='

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}

class maoyan:
    def __init__(self, url):
        self.url = url
        self.csvfile = open('data.csv', 'w', newline='')
        self.fieldnames = ['排名', '电影名', '演员', '上映时间', '评分']
        self.writer = csv.DictWriter(self.csvfile, fieldnames=self.fieldnames)
        self.writer.writeheader()
        self.data = []

    def set_url(self, num):
        result = self.url + str(num)
        return result

    def parse_one_page(self, url):
        try:
            res = requests.get(url, headers=headers)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, 'lxml')
            dds = soup.select('dd')
            if not dds:
                return
            for dd in dds:
                index = dd.select(".board-index")[0].text
                title = dd.select(".name")[0].text
                actors = dd.select('.star')[0].text.strip()[3:]
                time = dd.select('.releasetime')[0].text[5:]
                score = dd.select('.score')[0].text
                info = {
                    self.fieldnames[0]: index,
                    self.fieldnames[1]: title,
                    self.fieldnames[2]: actors,
                    self.fieldnames[3]: time,
                    self.fieldnames[4]: score
                }
                self.data.append(info)
        except Exception as exc:
            return

    def write_to_csv(self):
        for i in range(10):
            url = self.set_url(i * 10)
            self.parse_one_page(url)
        if self.data:
            self.writer.writerows(self.data)
            self.csvfile.close()


if __name__ == '__main__':
    m = maoyan(url)
    m.write_to_csv()