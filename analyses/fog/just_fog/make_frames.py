#!/usr/bin/env python

# Make 240 plots (10 seconds of video) evenly distributed 
#  across the data range#

import os
import datetime

current = datetime.date(1850,3,1)
while current<datetime.date(2015,12,31):
    opf = "%s/images/20CRv3_just_fog/%04d%02d%02d%02d.png" %\
                  (os.getenv('SCRATCH'),current.year,
                   current.month,current.day,12)
    if not os.path.isfile(opf):
        print("./20CRv3_released.py --year=%d --month=%d --day=%d --hour=%d" %
                (current.year,current.month,current.day,12))
    current =datetime.date(current.year+2,current.month,current.day)
