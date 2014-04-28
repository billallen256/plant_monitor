#!/usr/bin/env python

import sys
import time
from datetime import datetime, timedelta
from influxdb import client as influxdb

def parseTimestamp(ts):
	year = int(ts[0:4])
	month = int(ts[4:6])
	day = int(ts[6:8])
	hour = int(ts[8:10])
	minute = int(ts[10:12])
	second = int(ts[12:14])

	return datetime(year, month, day, hour, minute, second)

if __name__ == "__main__":
	endTimestamp = sys.argv[1] # YYYYMMDDhhmmss

	if len(endTimestamp) != 14:
		print 'Invalid timestamp format.'
		sys.exit(1)

	delta = timedelta(seconds=10, milliseconds=250) # attempting to account for the write time
	endTime = parseTimestamp(endTimestamp)
	f = open(sys.argv[2], 'r')
	db = influxdb.InfluxDBClient('localhost', 8086, 'root', 'root', 'plant')
	points = []

	for line in f:
		temp, hum, dew, moist = line.split(',')
		temp = float(temp)
		hum = float(hum)
		dew = float(dew)
		moist = float(moist)
		points.append([temp,hum,dew,moist])

	points.reverse() # so we can start with the endtime

	lastTime = endTime

	for point in points:
		point.append(time.mktime(lastTime.timetuple()))
		lastTime = lastTime - delta

	data = [{
		'points':points,
		'name':'readings',
		'columns':['temp','humidity','dew','moisture','time']
	}]

	db.write_points(data)
	f.close()
