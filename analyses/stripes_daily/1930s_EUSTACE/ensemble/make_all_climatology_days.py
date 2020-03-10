#!/usr/bin/env python

# Scripts to make climatology for each day of the year

import os
import datetime

current=datetime.date(1981,1,1)
while current.year==1981:
    if current.month==2 and current.day==29:
        current+=datetime.timedelta(days=1)
        continue
    opf=("%s/EUSTACE/1.0/"+
         "clim_1926-1935/%02d%02d.nc") % (os.getenv('SCRATCH'),
                                          current.month,current.day)
    if os.path.isfile(opf):
        current+=datetime.timedelta(days=1)
        continue
    print("./make_climatology_for_day.py --month=%d --day=%d" % (
                                      current.month,current.day))
    current+=datetime.timedelta(days=1)
