import IRData.twcr as twcr
import datetime

for version in ('2c','4.5.1'):
    for month in (1,2):
        dte=datetime.datetime(1953,month,1)
        twcr.fetch('prmsl',dte,version=version)
        twcr.fetch_observations(dte,version=version)

