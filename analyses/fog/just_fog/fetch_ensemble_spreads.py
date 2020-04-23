#!/usr/bin/env python

import os
import datetime
import IRData.twcr as twcr

start = datetime.date(1850,1,1)
end   = datetime.date(2015,12,31)

yrs=range(1851,2015)

opdir = "%s/20CR/version_3/ensemble_spreads/PRMSL" % os.getenv('SCRATCH')

for year in yrs:
    
    if os.path.exists("%s/prmsl.%04d.nc" % (opdir,year)): continue

    if year<1981:
        print("wget -P %s ftp://ftp.cdc.noaa.gov/Datasets/20thC_ReanV3/spreads/miscSI/prmsl.%04d.nc" % (opdir,year))
    else:
        print("wget -P %s ftp://ftp.cdc.noaa.gov/Datasets/20thC_ReanV3/spreads/miscMO/prmsl.%04d.nc" % (opdir,year))

