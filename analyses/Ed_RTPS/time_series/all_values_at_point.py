#!/usr/bin/env python

import datetime
import os

start = datetime.datetime(1903, 1, 1, 6)
end = datetime.datetime(1903, 9, 30, 18)

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--lat", help="Latitude", type=float, required=True)
parser.add_argument("--lon", help="Longitude (0-360)", type=float, required=True)
parser.add_argument("--var", help="Variable to extract", type=str, required=True)
parser.add_argument(
    "--version",
    help="20CR version ('3' or e.g. '4.6.5')",
    type=str,
    required=True,
)
args = parser.parse_args()

current = start
while current < end:
    opfile = (
        "%s/20CRv3_point_data/version_%s/%s/%04d/%02d/%02d/"
        + "%02d_00_%+07.2f_%+06.2f.pkl"
    ) % (
        os.getenv("SCRATCH"),
        args.version,
        args.var,
        current.year,
        current.month,
        current.day,
        current.hour,
        args.lon,
        args.lat,
    )
    if not os.path.isfile(opfile):
        print(
            (
                "%s/store_20CR_value_at_point.py --version=%s --year=%d --month=%d"
                + "  --day=%d --hour=%d --lat=%f --lon=%f --var=%s"
            )
            % (
                os.path.dirname(__file__),
                args.version,
                current.year,
                current.month,
                current.day,
                current.hour,
                args.lat,
                args.lon,
                args.var,
            )
        )
    current += datetime.timedelta(hours=3)
