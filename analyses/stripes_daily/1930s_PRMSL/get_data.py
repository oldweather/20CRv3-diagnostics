#!/usr/bin/env python

# Download the 20CRv3 sub-daily PRMSL.

import IRData.twcr as twcr
import datetime

for year in range(1926,1935):
    twcr.fetch('PRMSL',datetime.datetime(year,1,1),version='3')

