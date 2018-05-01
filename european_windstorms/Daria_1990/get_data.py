import Meteorographica.data.twcr as twcr

for version in ('2c','4.5.2'):
    twcr.fetch('prmsl',1990,1,version=version)
    twcr.fetch_observations(1990,1,version=version)

