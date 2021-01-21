l
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

# Get the obs files from the grib2 archive (on hsi)
originals_directory = (
    "/home/projects/incite11/ensda_" + "v%03d_archive_grb2_monthly" % args.version
)
# Get the list of start years
proc = subprocess.Popen(
    "hsi ls -l %s" % originals_directory,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    shell=True,
)
(out, err) = proc.communicate()
start_years = err.decode("utf8").split()  # Why does hsi put output in stderr?
start_years = [x for x in start_years if "ensda_%03d" % args.version in x]
start_years = [int(x[-4:]) for x in start_years]
if args.startyear not in start_years:
    raise Exception("%04d is not as available start year" % args.startyear)

# Get the list of files available for the selected month
proc = subprocess.Popen(
    "hsi ls -l %s/ensda_%03d_%04d/%04d/%04d%02d_*.tar"
    % (
        originals_directory,
        args.version,
        args.startyear,
        args.year,
        args.year,
        args.month,
    ),
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    shell=True,
)
(out, err) = proc.communicate()
file_list = err.decode("utf8").split()
obs_files = [x for x in file_list if "_psobs" in x]
if len(obs_files) < 1:
    raise Exception("Obs files not available in grib2 archive")

# Have the list of files to retrieve - sort them into tape order
tfile = tempfile.NamedTemporaryFile(delete=False, mode="w")
for fn in obs_files:
    tfile.write(
        "%s/ensda_%03d_%04d/%04d/%s\n"
        % (originals_directory, args.version, args.startyear, args.year, fn)
    )
var_files = []
for var in ("PRMSL", "PRATE", "TMP2m", "UGRD10m", "VGRD10m", "TMPS", "PWAT", "WEASD"):
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

# Run the obs files retrieval
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
for file in obs_files + var_files:
    fpn = "%s/%s" % (working_directory, file)
    if not os.path.isfile(fpn):
        raise Exception("Missing file %s" % fpn)

    proc = subprocess.Popen("cd %s; tar xf %s" % (working_directory, file), shell=True)
    (out, err) = proc.communicate()
    if out is not None or err is not None:
        raise Exception("Failed to untar %s/%s" % (working_directory, file))
