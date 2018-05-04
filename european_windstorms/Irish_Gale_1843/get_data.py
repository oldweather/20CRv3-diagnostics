import Meteorographica.data.twcr as twcr

twcr.fetch('prmsl',1843,1,version='4.5.1')
twcr.fetch_observations(1843,1,version='4.5.1')

# 20CRv2c has no released data for 1843 - I've used 
#  data from scout 3.5.4 instead, but this is not
#  publically available.
