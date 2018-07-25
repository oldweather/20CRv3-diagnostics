import IRData.twcr as twcr
import datetime

dte=datetime.datetime(1990,1,1)
for version in ('2c','4.5.2'):
    twcr.fetch('prmsl',dte,version=version)
    twcr.fetch_observations(dte,version=version)

