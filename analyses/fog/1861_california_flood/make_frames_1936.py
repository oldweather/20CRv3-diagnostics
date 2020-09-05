#!/usr/bin/env python

# Scripts to make a 20CRv3 plot for 1936/7

import os
import datetime

current = datetime.datetime(1936, 1, 7, 0)
while current.year < 1938:
    opf = "%s/images/20CRv3_1861_california_flood/%04d%02d%02d%02d00.png" % (
        os.getenv("SCRATCH"),
        current.year,
        current.month,
        current.day,
        current.hour,
    )
    if not os.path.isfile(opf):
        print(
            "./20CRv3_released.py --year=%d --month=%d --day=%d --hour=%d"
            % (current.year, current.month, current.day, current.hour)
        )
    current += datetime.timedelta(hours=1)
