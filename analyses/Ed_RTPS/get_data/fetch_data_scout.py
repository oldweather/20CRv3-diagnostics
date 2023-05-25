#!/usr/bin/env python

# Need to get the data from tape on cori, and use sshproxy before running this

import os
import datetime
import IRData.twcr as twcr

for version in ('4.6.1','4.6.3','4.6.5'):
    for var in ('observations','PRMSL','PRATE'):
        try:
            twcr.fetch(var, datetime.datetime(1902, 12, 1), version=version)
        except:
            print("Failed %s retrieval for %s 1930-%02d" % (var,version,12))
        for month in range(1,10):
            try:
                twcr.fetch(var, datetime.datetime(1903, month, 1), version=version)
            except:
                print("Failed %s retrieval for %s 1930-%02d" % (var,version,month))

