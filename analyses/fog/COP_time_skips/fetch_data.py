#!/usr/bin/env python

import datetime
import IRData.twcr as twcr
import time

start = datetime.date(1850, 1, 1)
end = datetime.date(2015, 12, 31)

yrs = []
current = start
count = 0
last = None
while current <= end:
    if last is None or current.year != last:
        yrs.append(current.year)
    last = current.year
    count = count + 1
    if count >= 100:
        count = 0
        if current.month == 2 and current.day == 29:
            current += datetime.timedelta(days=1)
        current = datetime.date(current.year + 10, current.month, current.day)
    current += datetime.timedelta(days=1)

for year in yrs:
    for var in ("UGRD10m", "VGRD10m", "PRMSL"):
        try:
            twcr.fetch(var, datetime.datetime(year, 3, 12, 6), version="3")
        except:
            time.sleep(300)
            twcr.fetch(var, datetime.datetime(year, 3, 12, 6), version="3")
