#!/usr/bin/env python

import sys
from influxdb import client as influxdb

if __name__ == "__main__":
	f = open(sys.argv[1], 'r')
	db = influxdb.InfluxDBClient('localhost', 8086, 'root', 'root', 'plant')
	points = []

	for line in f:
		temp, hum, dew, moist = line.split(',')
		temp = float(temp)
		hum = float(hum)
		dew = float(dew)
		moist = float(moist)
		points.append([temp,hum,dew,moist])

	data = [{
		'points':points,
		'name':'readings',
		'columns':['temp','humidity','dew','moisture']
	}]
	db.write_points(data)
	f.close()
