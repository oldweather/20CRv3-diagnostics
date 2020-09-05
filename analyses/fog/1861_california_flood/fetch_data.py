#!/usr/bin/env python

import time
import datetime
import IRData.twcr as twcr

for year in (1936, 1937):
    for var in ("PRATE", "UGRD10m", "VGRD10m", "TMP2m", "PRMSL", "observations"):
        twcr.fetch(var, datetime.datetime(year, 3, 12, 6), version="3")
        time.sleep(1)
