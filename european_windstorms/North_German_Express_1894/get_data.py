import Meteorographica.data.twcr as twcr

for version in ('2c','4.5.1'):
    twcr.fetch('prmsl',1894,2,version=version)
    twcr.fetch_observations(1894,2,version=version)

