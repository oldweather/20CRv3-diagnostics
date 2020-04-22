#!/usr/bin/env python

import datetime
import IRData.twcr as twcr

start = datetime.date(1850,1,1)
end   = datetime.date(2015,12,31)

yrs=[]
current = start
count=0
last=None
while current<=end:
    if last is None or current.year != last:
        yrs.append(current.year)
    last = current.year
    count = count+1
    if count>=100:
        count=0
        if current.month==2 and current.day==29:
            current += datetime.timedelta(days=1)
        current = datetime.date(current.year+10,current.month,current.day)
    current += datetime.timedelta(days=1)

for year in yrs:
    if year<1981:
        print("wget ftp://ftp.cdc.noaa.gov/Datasets/20thC_ReanV3/spreads/miscSI/prmsl.%04d.nc" % year)
    else:
        print("wget ftp://ftp.cdc.noaa.gov/Datasets/20thC_ReanV3/spreads/miscMO/prmsl.%04d.nc" % year)

