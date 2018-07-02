import IRData.twcr as twcr
import datetime

for version in ('2c','4.5.1'):
    dtn=datetime.datetime(1961,9,1)
    twcr.fetch('prmsl',dtn,version=version)
    twcr.fetch_observations(dtn,version=version)

