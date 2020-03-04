#!/usr/bin/env python

# Download the 20CRv3 sub-daily PRATE.

import IRData.twcr as twcr
import datetime

for year in range(1926,1936):
    twcr.fetch('PRATE',datetime.datetime(year,1,1),version='3')

