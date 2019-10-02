#!/usr/bin/env python

# Get a year's data for selected variables from the final 20CRv3 archives and 
#  package it into a tar file for downloading.

import os
import sys
import subprocess

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--year", help="Year run started",
                    type=int, required=True)
args = parser.parse_args()

# Get a fixed set of variables
vars=('TMP2m','U10M','V10M','PRATE','PRMSL','ICEC')

# Store the results in $SCRATCH
opdir="%s/20CR/version_3/%04d" % (os.getenv('SCRATCH'),args.year)
if not os.path.isdir(opdir):
    os.makedirs(opdirs)

# Get the data off hsi
if args.year<=1980:
    originals_directory="/home/projects/incite11/20CR_v3_451_ncfiles/"
else:
    originals_directory="/home/projects/incite11/20CR_v3_452_ncfiles/"

for var in vars:
    cmd="hsi cget %s/%s_%04d_v3.tar" % (originals_directory,var,args.year)
    proc = subprocess.Popen(cmd, shell=True)
    (out, err) = proc.communicate()
    proc = subprocess.Popen("cd %s; tar xf %s_%04d_v3.tar" % (
                            opdir,var,args.year), shell=True)
    (out, err) = proc.communicate()

