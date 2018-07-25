import IRData.twcr as twcr
import datetime

dte=datetime.datetime(1843,1,1)
twcr.fetch('prmsl',dte,version='4.5.1')
twcr.fetch_observations(dte,version='4.5.1')

# 20CRv2c has no released data for 1843 - I've used 
#  data from scout 3.5.4 instead, but this is not
#  publically available.
