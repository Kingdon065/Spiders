#! python3
# _*_ coding: utf-8 _*_
"""
@Project: Tickets
@Author: masiyuan
@Time: 2018/12/1 0:30
"""

from urllib.parse import quote, unquote

s = '昭通'
print(quote(s))
print(quote('%u4E0A%u6D77'))

