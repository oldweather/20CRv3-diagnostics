#!/usr/bin/env python

# Clean up all the 20CR data used to make the NetCDF files

import argparse
import os
import glob
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("--startyear", help="Year run started", type=int, required=True)
parser.add_argument("--year", help="Year", type=int, required=True)
parser.add_argument("--month", help="Month", type=int, required=True)
parser.add_argument("--version", help="Version", type=int, default=451)
args = parser.parse_args()

final_directory = "%s/20CRv3.final/version_%1d.%1d.%1d/%04d/%02d" % (
    os.getenv("SCRATCH"),
    int(args.version / 100),
    int((args.version % 100) / 10),
    int(args.version % 10),
    args.year,
    args.month,
)
# Final grib files
fgf = glob.glob("%s/*.grb2" % final_directory)
for gf in fgf:
    os.remove(gf)

# Raw output from tape
working_directory = "%s/20CRv3.working/ensda_%04d/%04d/%02d" % (
    os.getenv("SCRATCH"),
    args.startyear,
    args.year,
    args.month,
)
shutil.rmtree(working_directory)
