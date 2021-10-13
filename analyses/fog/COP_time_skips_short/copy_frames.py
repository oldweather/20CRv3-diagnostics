#!/usr/bin/env python

# Scripts to make a 20CRv3 plot for a range of days

import os
import datetime

years = (
    1860,
    1880,
    1901,
    1921,
    1942,
    1963,
    1983,
    2004,
)

ycount = 0
current = datetime.datetime(years[ycount], 3, 1, 0)
count = 0
while ycount < len(years):
    opf = "%s/images/COP_time_skips/%04d%02d%02d%02d00.png" % (
        os.getenv("SCRATCH"),
        2015 - current.year,
        current.month,
        current.day,
        current.hour,
    )
    print("cp %s %s/images/COP_time_skips_short" % (opf, os.getenv("SCRATCH")))
    current += datetime.timedelta(hours=1)
    count = count + 1
    if count >= 120:
        count = 0
        ycount += 1
        if ycount < len(years):
            current = datetime.datetime(years[ycount], 3, 1, 0)
