#!/usr/bin/env python

# Download the 20CRv3 data for the period around the floods

import IRData.twcr as twcr
import datetime
import time

for year in [1931]:
    try:
        twcr.fetch("observations", datetime.datetime(year, 1, 1), version="3")
    except:
        time.sleep(300)
        twcr.fetch("observations", datetime.datetime(year, 1, 1), version="3")
    try:
        twcr.fetch("PRMSL", datetime.datetime(year, 1, 1), version="3")
    except:
        time.sleep(300)
        twcr.fetch("PRMSL", datetime.datetime(year, 1, 1), version="3")
    try:
        twcr.fetch("UGRD10m", datetime.datetime(year, 1, 1), version="3")
    except:
        time.sleep(300)
        twcr.fetch("UGRD10m", datetime.datetime(year, 1, 1), version="3")
    try:
        twcr.fetch("VGRD10m", datetime.datetime(year, 1, 1), version="3")
    except:
        time.sleep(300)
        twcr.fetch("VGRD10m", datetime.datetime(year, 1, 1), version="3")
