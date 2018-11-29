#! python3

from stations import stations
from pprint import pprint

temp = dict(zip(stations.values(), stations.keys()))

pprint(temp, indent=4)