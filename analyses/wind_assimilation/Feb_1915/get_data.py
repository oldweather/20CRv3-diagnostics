import datetime
import v3_fetch
import scout_fetch

v3_fetch.fetch("PRMSL", datetime.datetime(1915, 2, 15))
v3_fetch.fetch_observations(datetime.datetime(1915, 2, 15))

scout_fetch.fetch("prmsl", datetime.datetime(1915, 2, 15), version="5.7.6")
scout_fetch.fetch_observations(datetime.datetime(1915, 2, 15), version="5.7.6")
