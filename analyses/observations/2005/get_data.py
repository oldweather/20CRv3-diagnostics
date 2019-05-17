#!/usr/bin/env python

import IRData.twcr as twcr
import datetime

dte=datetime.datetime(2005,9,1)

twcr.fetch('observations',dte,version='4.5.2')
twcr.fetch('prmsl',dte,version='4.5.2')

