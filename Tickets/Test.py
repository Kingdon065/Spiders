#! python3
# _*_ coding: utf-8 _*_
"""
@Project: Tickets
@Author: masiyuan
@Time: 2018/12/1 0:30
"""

from colorama import init, Fore, Back, Style
init(autoreset=True)
print(Fore.RED + 'some blue text')
print(Back.CYAN + 'cyan background')
print(Style.DIM + 'in dim text')
print('auto set to normal now')