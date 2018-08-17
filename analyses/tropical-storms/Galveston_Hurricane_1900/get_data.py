#!/usr/bin/env python

import IRData.twcr as twcr
import datetime

for version in ('2c','4.5.1'):
    for month in [9]:
        dtn=datetime.datetime(1900,month,1)
        twcr.fetch('prmsl',dtn,version=version)
        twcr.fetch_observations(dtn,version=version)

