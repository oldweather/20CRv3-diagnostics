#!/usr/bin/env python

import IRData.twcr as twcr
import datetime

dte=datetime.datetime(1902,8,1)

twcr.fetch('observations',dte,version='4.5.1')
twcr.fetch('prmsl',dte,version='4.5.1')

