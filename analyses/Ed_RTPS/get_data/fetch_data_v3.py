#!/usr/bin/env python

import os
import time
import datetime
import IRData.twcr as twcr

# disable ssh agent so superjanet wget works
os.environ['SSH_AUTH_SOCK'] = ''

for year in (1902,1903):
    for var in ('observations','PRMSL','PRATE'):
        try:
            twcr.fetch(var,datetime.datetime(year,3,12),version='3')
        except:
            time.sleep(300)
            twcr.fetch(var,datetime.datetime(year,3,12),version='3')

