#!/usr/bin/env python

# Download the 20CRv3 sub-daily T2m.

import IRData.twcr as twcr
import datetime

for year in range(2006,2016):
    twcr.fetch('TMP2m',datetime.datetime(year,1,1),version='3')

