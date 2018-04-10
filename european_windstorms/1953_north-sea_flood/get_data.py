import Meteorographica.data.twcr as twcr

for version in ('2c','4.5.1'):
    for month in (1,2):
        twcr.fetch('prmsl',1953,month,version=version)
        twcr.fetch_observations(1953,month,version=version)

