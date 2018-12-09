#! python3
# _*_ coding: utf-8 _*_
"""
@Project: Tickets
@Author: masiyuan
@Time: 2018/12/1 0:30
"""

import json
import requests, sys
import argparse
from prettytable import PrettyTable
from urllib.parse import urlencode
from Stations.stations import stations
from Stations.stations2 import stations2
from Color.color import Colored


class Tickets:
    def __init__(self, args):
        self.args = args
        self.data = None
        fields = '车次 车站 时间 历时 特等 一等 二等 高级软卧 软卧 动卧 硬卧 软座 硬座 无座 备注'.split()
        self.table = PrettyTable(fields)
        self.color = Colored()

    def get_data(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
        base_url = 'https://kyfw.12306.cn/otn/leftTicket/query?'
        purpose_codes = 'ADULT'
        if self.args.is_student:
            purpose_codes = '0X00'
        try:
            params = {
                'leftTicketDTO.train_date': self.args.info[2],
                'leftTicketDTO.from_station': stations[self.args.info[0]],
                'leftTicketDTO.to_station': stations[self.args.info[1]],
                'purpose_codes': purpose_codes
            }
            url = base_url + urlencode(params)

            response = requests.get(url, headers=headers)
            response.encoding = 'utf-8'
            self.data = response.json()
        except json.decoder.JSONDecodeError:
            error = self.color.red('Error:')
            text = self.color.yellow('输入日期错误或不在正常售票时间范围之内(一般为即日起30天内)!')
            print(f'{error} {text}')
            sys.exit()
        except KeyError:
            error = self.color.red('Error:')
            text = self.color.yellow('输入站点不正确!')
            print(f'{error} {text}')
            sys.exit()

    def insert_data(self, row):
        # 字体着色
        train_code = self.color.yellow(row[3])              # 车次
        from_station = self.color.green(stations2[row[6]])  # 出发站
        start_time = self.color.green(row[8])               # 出发时间

        lasted = row[10]            # 历时
        principal_seat = row[32]    # 特等座
        first_class_seat = row[31]  # 一等座
        second_class_seat = row[30] # 二等座
        premium_soft = row[21]      # 高级软卧
        soft_sleep = row[23]        # 软卧
        move_sleep = row[33]        # 动卧
        hard_sleep = row[28]        # 硬卧
        soft_seat = row[24]         # 软座
        hard_seat = row[29]         # 硬座
        no_seat = row[26]           # 无座
        note = row[0]               # 备注

        self.table.add_row([train_code, from_station, start_time, lasted, principal_seat,
                            first_class_seat, second_class_seat, premium_soft, soft_sleep,
                            move_sleep, hard_sleep, soft_seat, hard_seat, no_seat, note])
        next_line = [''] * 15
        next_line[1] = self.color.red(stations2[row[7]])     # 到达站
        next_line[2] = self.color.red(row[9])                # 到达时间
        self.table.add_row(next_line)

    def show(self):
        flag = False
        for result in self.data['data']['result']:
            row = result.split('|')
            # 秘密字符串存在表示有票，否则没有
            if row[0] != '':
                row[0] = '预订'
                row[0] = self.color.blue(row[0])

            for i in range(len(row)):
                if row[i] == '':
                    row[i] = '-'
                if row[i] == '有':
                    row[i] = self.color.green(row[i])

            if self.args.is_gao:
                flag = True
                if row[3][0] == 'G':
                    self.insert_data(row)
            if self.args.is_dong:
                flag = True
                if row[3][0] == 'D':
                    self.insert_data(row)
            if self.args.is_tekuai:
                flag = True
                if row[3][0] == 'T':
                    self.insert_data(row)
            if self.args.is_kuai:
                flag = True
                if row[3][0] == 'K':
                    self.insert_data(row)
            if self.args.is_zhida:
                flag = True
                if row[3][0] == 'Z':
                    self.insert_data(row)
            if not flag:
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
        metavar=('from', 'to', 'date'),     # 分别指定3个参数的显示名称
        help='输入起始站点(如北京)，到达站点(如上海)，时间(格式: 2018-01-01)'
    )
    parse.add_argument(
        '-G',
        action='store_true',
        dest='is_gao',
        default=False,
        help='高铁'
    )
    parse.add_argument(
        '-D',
        action='store_true',
        dest='is_dong',
        default=False,
        help='动车'
    )
    parse.add_argument(
        '-T',
        action='store_true',
        dest='is_tekuai',
        default=False,
        help='特快列车'
    )
    parse.add_argument(
        '-K',
        action='store_true',
        dest='is_kuai',
        default=False,
        help='快速列车'
    )
    parse.add_argument(
        '-Z',
        action='store_true',
        dest='is_zhida',
        default=False,
        help='直达列车'
    )
    parse.add_argument(
        '-v',
        '--version',
        action='version',
        version='%(prog)s: version 1.0.6',
        help='显示版本信息'
    )
    parse.add_argument(
        '--student',
        action='store_true',
        dest='is_student',
        default=False,
        help='学生票'
    )
    args = parse.parse_args()

    tickets = Tickets(args)
    tickets.get_data()
    tickets.show()


if __name__ == '__main__':
    run()