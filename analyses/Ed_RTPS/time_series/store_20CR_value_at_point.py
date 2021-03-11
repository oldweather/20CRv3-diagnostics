#!/usr/bin/env python

# Extract data from 20CRv3 (or a scout run) at a given time and place
#   and store the value on SCRATCH.

import IRData.twcr as twcr
import iris
import iris.analysis
import numpy
import datetime
import pickle
import os

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--year", help="Year", type=int, required=True)
parser.add_argument("--month", help="Month", type=int, required=True)
parser.add_argument("--day", help="Day", type=int, required=True)
parser.add_argument("--hour", help="Hour (and fraction)", type=float, required=True)
parser.add_argument("--lat", help="Latitude", type=float, required=True)
parser.add_argument("--lon", help="Longitude (0-360)", type=float, required=True)
parser.add_argument("--var", help="Variable to extract", type=str, required=True)
parser.add_argument(
    "--version",
    help="20CR version ('3' or e.g. '4.6.5')",
    default="3",
    type=str,
    required=True,
)
parser.add_argument(
    "--opdir",
    help="Directory for output files",
    default="%s/20CRv3_point_data" % os.getenv("SCRATCH"),
    type=str,
    required=False,
)
args = parser.parse_args()

args.opdir = "%s/version_%s/%s/%04d/%02d/%02d" % (
    args.opdir,
    args.version,
    args.var,
    args.year,
    args.month,
    args.day,
)
if not os.path.isdir(args.opdir):
    os.makedirs(args.opdir)

dte = datetime.datetime(
    args.year, args.month, args.day, int(args.hour), int((args.hour % 1) * 60)
)
rdata = twcr.load(args.var, dte, version=args.version)
interpolator = iris.analysis.Linear().interpolator(rdata, ["latitude", "longitude"])
ensemble = interpolator([numpy.array(args.lat), numpy.array(args.lon)]).data

pickle.dump(
    ensemble,
    open(
        "%s/%02d_%02d_%+07.2f_%+06.2f.pkl"
        % (args.opdir, int(args.hour), int((args.hour % 1) * 60), args.lon, args.lat),
        "wb",
    ),
)
