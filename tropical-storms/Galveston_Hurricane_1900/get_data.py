import Meteorographica.data.twcr as twcr

for version in ('2c','4.5.1'):
    for month in (8,9):
        twcr.fetch('prmsl',1900,month,version=version)
        twcr.fetch_observations(1900,month,version=version)

