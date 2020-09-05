#!/usr/bin/env python

for year in (1861, 1862, 1936, 1937):
    if year < 1981:
        print(
            "wget ftp://ftp.cdc.noaa.gov/Datasets/20thC_ReanV3/spreads/miscSI/prmsl.%04d.nc"
            % year
        )
    else:
        print(
            "wget ftp://ftp.cdc.noaa.gov/Datasets/20thC_ReanV3/spreads/miscMO/prmsl.%04d.nc"
            % year
        )
