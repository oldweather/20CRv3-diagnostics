import Meteorographica.data.twcr as twcr

for version in ('2c','4.5.2'):
    twcr.fetch('prmsl',1999,12,version=version)
    twcr.fetch_observations(1999,12,version=version)

