#!/usr/bin/env python

import IRData.twcr as twcr
import datetime

dte=datetime.datetime(2005,9,1)

twcr.fetch('observations',dte,version='4.5.2')
twcr.fetch('prmsl',dte,version='4.5.2')
twcr.fetch('tmp',dte,level=850,version='4.5.2')

twcr.fetch('observations',dte,version='2c')
twcr.fetch('prmsl',dte,version='2c')
twcr.fetch('t850',dte,version='2c')
