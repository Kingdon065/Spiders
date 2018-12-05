#! python3
# _*_ coding: utf-8 _*_


from Stations.stations import stations
from pprint import pprint

temp = dict(zip(stations.values(), stations.keys()))

pprint(temp, indent=4)