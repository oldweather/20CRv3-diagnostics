#!/usr/bin/env python

# Scripts to make slices for every month

import os
import datetime
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--min_lat", help="Min latitude",
                    type=float,required=False,default=-90.0)
parser.add_argument("--max_lat", help="Max latitude",
                    type=float,required=False,default=90.0)
parser.add_argument("--min_lon", help="Min longitude",
                    type=float,required=False,default=-180.0)
parser.add_argument("--max_lon", help="Max longitude",
                    type=float,required=False,default=360.0)
args = parser.parse_args()

for year in range (1806,2016):
    print(("./get_slice.py --year=%d "+
           "--min_lat=%f --max_lat=%f "+
           "--min_lon=%f --max_lon=%f") % (year,
            args.min_lat,args.max_lat,
            args.min_lon,args.max_lon))
