#!/usr/bin/env python

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
parser.add_argument("--startyear", help="Year run started",
                    type=int, required=True)
parser.add_argument("--year", help="Year to extract",
                    type=int, required=True)
parser.add_argument("--month", help="Month to extract",
                    type=int, required=True)
parser.add_argument("--version", help="Month to extract",
                    type=int,default=451)
args = parser.parse_args()

# Location of Output files (on hsi)
originals_directory="/home/projects/incite11/ensda_"+\
                    "v%03d_holdspinup" % args.version
# Where to put the grib (and obs) files retrieved from hsi
working_directory="%s/20CRv3.working.orig/ensda_%04d/%04d/%02d" % (
                   os.getenv('SCRATCH'),args.startyear,
                   args.year,args.month)
if not os.path.isdir(working_directory):
    os.makedirs(working_directory)

# Get the list of start years
proc = subprocess.Popen("hsi ls -l %s" % originals_directory,
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
start_years=err.split() # Why does hsi put output in stderr?
start_years=filter(lambda x:'ensda_%03d' % args.version in x, start_years)
start_years=[int(x[-4:]) for x in start_years]
if args.startyear not in start_years:
    raise StandardError(
      "%04d is not as available start year" % args.startyear)

# Get the list of files available for the selected month
proc = subprocess.Popen("hsi ls -l %s/ensda_%03d_%04d/%04d%02d*.tar" % (
                    originals_directory,args.version,
                    args.startyear,args.year,
                    args.month),
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
file_list=err.split()
tar_files=filter(lambda x: '%04d%02d' % (args.year,args.month) in x, file_list)
if len(tar_files)<100:
    print file_list
    raise StandardError("Data not available")

# Have the list of files to retrieve - sort them into tape order
tfile=tempfile.NamedTemporaryFile(delete=False)
for fn in tar_files:
    tfile.write("%s/ensda_%03d_%04d/%s\n" % (
                    originals_directory,args.version,
                    args.startyear,fn))
tfile.close()
sfile=tempfile.NamedTemporaryFile(delete=False)
proc = subprocess.Popen("hpss_file_sorter.script %s > %s" % (
                         tfile.name,sfile.name),
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
# Doesn't work - for now, assume success.
#if out is not None or err is not None:
    #raise StandardError("Problem with hsi tape ordering")

# Run the retrieval - may take a long time
sfile.close()
sfile=open(sfile.name,'r')
tfile=open(tfile.name,'w')
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
for file in tar_files:
    fpn= "%s/%s" % (working_directory,file)
    if not os.path.isfile(fpn):
        raise StandardError("Missing file %s" % fpn)
         
    proc = subprocess.Popen("cd %s; tar xf %s" % (
                            working_directory,file), shell=True)
    (out, err) = proc.communicate()
    if out is not None or err is not None:
        raise StandardError("Failed to untar %s/%s" % (
                             working_directory,file))

