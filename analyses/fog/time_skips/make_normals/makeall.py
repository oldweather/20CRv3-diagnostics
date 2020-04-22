#!/usr/bin/env python

# Scripts to make normals for every 3-hours

import os
import datetime

startyear=1969  # Any non leap year is fine
var='TMP2m'

op_dir = "%s/20CR/version_3/normals/%s/climatology_1981_2010" % (
          os.getenv('DATADIR'),var)

cdy = datetime.datetime(startyear,1,1,0)
while cdy.year==startyear:
    opf = "%s/%02d%02d%02d.nc" % (op_dir,cdy.month,cdy.day,cdy.hour) 
    if not os.path.isfile(opf):
        print("./make_normal_at_time.py --var=%s --month=%d --day=%d --hour=%d" %
                (var,cdy.month,cdy.day,cdy.hour))
    cdy += datetime.timedelta(hours=3)
