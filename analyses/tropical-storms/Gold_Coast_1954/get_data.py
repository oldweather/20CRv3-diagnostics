#!/usr/bin/env python

import IRData.twcr as twcr
import datetime

dte=datetime.datetime(1954,2,1)
for version in ('2c','4.5.1'):
    twcr.fetch('prmsl',dte,version=version)
    twcr.fetch_observations(dte,version=version)

