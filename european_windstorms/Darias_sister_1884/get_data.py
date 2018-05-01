import Meteorographica.data.twcr as twcr

for version in ('2c','4.5.1'):
    twcr.fetch('prmsl',1884,1,version=version)
    twcr.fetch_observations(1884,1,version=version)

