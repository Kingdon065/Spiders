#! python3

import requests
import argparse
from prettytable import PrettyTable
from urllib.parse import urlencode
from stations import stations
from stations2 import stations2


class Tickets:
    def __init__(self, args):
        self.args = args
        self.data = None
        fields = '车次 车站 时间 历时 特等 一等 二等 高级软卧 软卧 动卧 硬卧 软座 硬座 无座'.split()
        self.table = PrettyTable(fields)

    def get_data(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
        base_url = 'https://kyfw.12306.cn/otn/leftTicket/query?'
        params = {
            'leftTicketDTO.train_date': self.args.info[2],
            'leftTicketDTO.from_station': stations[self.args.info[0]],
            'leftTicketDTO.to_station': stations[self.args.info[1]],
            'purpose_codes': 'ADULT'
        }
        url = base_url + urlencode(params)

        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        self.data = response.json()

    def insert_data(self, row):
        self.table.add_row([row[3], stations2[row[6]], row[8], row[10], row[32], row[31], row[30],
                       row[21], row[23], row[33], row[28], row[24], row[29], row[26]])
        temp = [''] * 14
        temp[1] = stations2[row[7]]
        temp[2] = row[9]
        self.table.add_row(temp)

    def show(self):
        for result in self.data['data']['result']:
            row = result.split('|')
            for i in range(len(row)):
                if row[i] == '':
                    row[i] = '-'

            if self.args.is_gao:
                if row[3][0] == 'G':
                    self.insert_data(row)
            elif self.args.is_dong:
                if row[3][0] == 'D':
                    self.insert_data(row)
            elif self.args.is_tekuai:
                if row[3][0] == 'T':
                    self.insert_data(row)
            elif self.args.is_kuai:
                if row[3][0] == 'K':
                    self.insert_data(row)
            else:
                self.insert_data(row)

        self.table.align['车次'] = 'l'
        self.table.padding_width = 1
        print(f'\n出发地: {self.args.info[0]}  目的地: {self.args.info[1]}  日期: {self.args.info[2]}\n')
        print(self.table)


def run():
    parse = argparse.ArgumentParser(
        prog='tickets',
        description='查询火车票车次信息，默认查询全部车次类型'
    )
    parse.add_argument(
        '-i',
        '--info',
        nargs=3,
        required=True,
        help='输入起始站点(如北京)，到达站点(如上海)，时间(格式: 2018-01-01)'
    )
    parse.add_argument(
        '-G',
        action='store_true',
        dest='is_gao',
        default=False,
        help='只查询高铁'
    )
    parse.add_argument(
        '-D',
        action='store_true',
        dest='is_dong',
        default=False,
        help='只查询动车'
    )
    parse.add_argument(
        '-T',
        action='store_true',
        dest='is_tekuai',
        default=False,
        help='只查询特快列车'
    )
    parse.add_argument(
        '-K',
        action='store_true',
        dest='is_kuai',
        default=False,
        help='只查询快速列车'
    )
    args = parse.parse_args()

    tickets = Tickets(args)
    tickets.get_data()
    tickets.show()


if __name__ == '__main__':
    run()