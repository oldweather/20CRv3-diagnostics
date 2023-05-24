#!/usr/bin/env python3

# Extract 20CRv3 data for a month - from tape to $SCRATCH
# This version uses Chesley's new monthly netCDF files

import os
import sys
import subprocess
import tempfile
import datetime
from shutil import copyfile

# Version and month
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--startyear", help="Year run started", type=int, required=True)
parser.add_argument("--year", help="Year to extract", type=int, required=True)
parser.add_argument("--month", help="Month to extract", type=int, required=True)
parser.add_argument("--version", help="Scout run number", type=int, default=451)
args = parser.parse_args()

# Where to put the grib (and obs) files retrieved from hsi
working_directory = "%s/20CRv3.working.nc/version_%03d/%04d/%02d" % (
    os.getenv("SCRATCH"),
    args.version,
    args.year,
    args.month,
)
if not os.path.isdir(working_directory):
    os.makedirs(working_directory)


# Have the list of files to retrieve - sort them into tape order
tfile = tempfile.NamedTemporaryFile(delete=False, mode="w")
var_files = []
for var in ("WATRsfc", "SOIL0-10cm"):
    var_files.append(
        "%s_%04d%02d_v3_x%03d.tar" % (var, args.year, args.month, args.version)
    )
    tfile.write(
        (
            "/home/projects/incite11/20CR_v3_%03d_ncfiles/"
            + "%s/%s_%04d%02d_v3_x%03d.tar\n"
        )
        % (args.version, var, var, args.year, args.month, args.version)
    )
tfile.close()
sfile = tempfile.NamedTemporaryFile(delete=False, mode="w")
proc = subprocess.Popen(
    "hpss_file_sorter.script %s > %s" % (tfile.name, sfile.name),
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    shell=True,
)
(out, err) = proc.communicate()
# Doesn't work - for now, assume success.
# if out is not None or err is not None:
# raise StandardError("Problem with hsi tape ordering")

# Run the  retrieval
sfile.close()
sfile = open(sfile.name, "r")
tfile = open(tfile.name, "w")
tfile.write("lcd %s\n" % working_directory)
for line in sfile:
    tfile.write("cget %s" % line)
sfile.close()
tfile.close()
os.remove(sfile.name)
proc = subprocess.Popen("hsi < %s" % tfile.name, shell=True)
(out, err) = proc.communicate()
os.remove(tfile.name)

# Check that the files retrieved, and untar
for file in var_files:
    fpn = "%s/%s" % (working_directory, file)
    if not os.path.isfile(fpn):
        raise Exception("Missing file %s" % fpn)

    proc = subprocess.Popen("cd %s; tar xf %s" % (working_directory, file), shell=True)
    (out, err) = proc.communicate()
    if out is not None or err is not None:
        raise Exception("Failed to untar %s/%s" % (working_directory, file))
