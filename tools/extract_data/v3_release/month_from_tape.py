#!/usr/bin/env python3

# Extract 20CRv3 data for a month - from tape to $SCRATCH

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
parser.add_argument("--version", help="Month to extract", type=int, default=451)
args = parser.parse_args()

# Location of Output files (on hsi)
originals_directory = (
    "/home/projects/incite11/ensda_" + "v%03d_archive_grb2_monthly" % args.version
)
# Where to put the grib (and obs) files retrieved from hsi
working_directory = "%s/20CRv3.working/ensda_%04d/%04d/%02d" % (
    os.getenv("SCRATCH"),
    args.startyear,
    args.year,
    args.month,
)
if not os.path.isdir(working_directory):
    os.makedirs(working_directory)

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
    raise Exception("Data not available")
anl_files = [x for x in file_list if "_pgrbanl_" in x]
if len(anl_files) < 80:
    raise Exception("Analysis data not complete")
fg_files = [x for x in file_list if "_pgrbfg_" in x]
if len(fg_files) < 80:
    raise Exception("Forecast data not complete")


# Have the list of files to retrieve - sort them into tape order
tfile = tempfile.NamedTemporaryFile(delete=False, mode="w")
for fn in obs_files + anl_files + fg_files:
    tfile.write(
        "%s/ensda_%03d_%04d/%04d/%s\n"
        % (originals_directory, args.version, args.startyear, args.year, fn)
    )
tfile.close()
sfile = tempfile.NamedTemporaryFile(delete=False, mode="w")
proc = subprocess.Popen(
    (
        "generate_sorted_list_for_hpss.py -i %s |"
        + "grep -v 'Generating sorted list from input file' > %s"
    )
    % (tfile.name, sfile.name),
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    shell=True,
)
(out, err) = proc.communicate()

# Doesn't work - for now, assume success.
# if out is not None or err is not None:
# raise StandardError("Problem with hsi tape ordering")

# Run the retrieval - may take a long time
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
for file in obs_files + anl_files + fg_files:
    fpn = "%s/%s" % (working_directory, file)
    if not os.path.isfile(fpn):
        raise Exception("Missing file %s" % fpn)

    proc = subprocess.Popen("cd %s; tar xf %s" % (working_directory, file), shell=True)
    (out, err) = proc.communicate()
    if out is not None or err is not None:
        raise Exception("Failed to untar %s/%s" % (working_directory, file))
