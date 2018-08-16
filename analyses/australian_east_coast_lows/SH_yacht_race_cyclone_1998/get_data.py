#!/usr/bin/env python

import IRData.twcr as twcr
import datetime

dte=datetime.datetime(1998,12,1)
for version in ('2c','4.5.2'):
    twcr.fetch('prmsl',dte,version=version)
    twcr.fetch_observations(dte,version=version)

