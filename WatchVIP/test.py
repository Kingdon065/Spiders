#! python3

import requests

f = open('source.txt')

lines = f.readlines()

obj1 = []
obj2 = []

for line in lines:
    tmp = line.split()
    obj1 += tmp
f.close()

f = open('last.txt')
lines = f.readlines()

for line in lines:
    tmp = line.split()
    obj2 += tmp
f.close()

for l in obj2:
    if l not in obj1:
        print(l)
