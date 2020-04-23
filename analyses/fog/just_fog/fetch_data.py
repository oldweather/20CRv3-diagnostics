#!/usr/bin/env python

import datetime
import IRData.twcr as twcr

for var in ('PRATE','UGRD10m','VGRD10m','TMP2m','observations'):
    twcr.fetch(var,datetime.datetime(2014,3,12,6),version='3')
