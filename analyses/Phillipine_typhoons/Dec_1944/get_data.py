#!/usr/bin/env python

import IRData.twcr as twcr
import datetime

dte=datetime.datetime(1944,12,1)
for version in ('3','2c'):
    twcr.fetch('prmsl',dte,version=version)
    #twcr.fetch('prate',dte,version=version)
    twcr.fetch_observations(dte,version=version)

