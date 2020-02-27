#!/usr/bin/env python3

# Get a year's data for selected variables from the final 20CRv3 archives and 
#  package it into a tar file for downloading.

import os
import sys
import subprocess
import datetime
from shutil import copyfile

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--year", help="Year run started",
                    type=int, required=True)
args = parser.parse_args()

# Get a fixed set of variables
vars=('TMP2m','UGRD10m','VGRD10m','PRATE','PRMSL')

# Store the results in $SCRATCH
opdir="%s/20CR/version_3/" % os.getenv('SCRATCH')
if not os.path.isdir(opdir):
    os.makedirs(opdir)

# Get the data off hsi
if args.year<=1980:
    originals_directory="/home/projects/incite11/20CR_v3_451_ncfiles/"
else:
    originals_directory="/home/projects/incite11/20CR_v3_452_ncfiles/"

for var in vars:
    cmd="cd %s; hsi cget %s/%s/%s_%04d_v3.tar" % (opdir,
                                                  originals_directory,
                                                  var,var,args.year)
    proc = subprocess.Popen(cmd, shell=True)
    (out, err) = proc.communicate()
    proc = subprocess.Popen("cd %s; tar xf %s_%04d_v3.tar" % (
                            opdir,var,args.year), shell=True)
    (out, err) = proc.communicate()
    # Compress all the files
    for mem in range(1,81):
        fname="%04d/%s.%04d_mem%03d.nc" % (args.year,var,args.year,mem)
        cname="%04d/%s.%04d_mem%03d_cmp.nc" % (args.year,var,args.year,mem)
        cmd="cd %s; module load ncview; nccopy -s -d 2 %s %s ; mv %s %s" % (
            opdir,fname,cname,cname,fname)
        proc = subprocess.Popen(cmd, shell=True)
        (out, err) = proc.communicate()

# Add the obs
ensda=args.year-args.year%5
if ensda==args.year: ensda=ensda-5
ensda=ensda-1
if args.year>1980:
    sourcedir="/project/projectdirs/incite11/ensda_v452/ensda_%04d" % ensda
else:
    sourcedir="/project/projectdirs/incite11/ensda_v451/ensda_%04d" % ensda
o_opdir="%s/%04d/observations" % (opdir,args.year)
if not os.path.isdir(o_opdir):
    os.makedirs(o_opdir)
current=datetime.datetime(args.year,1,1,0,0)
while current.year==args.year:
    source_file="%s/%04d%02d%02d%02d/psobs_posterior.txt" % (sourcedir,
                     current.year,current.month,current.day,current.hour)
    target_file="%s/%04d%02d%02d%02d_psobs_posterior.txt" % (
                     o_opdir,
                     current.year,current.month,current.day,current.hour)
    if not os.path.isfile(source_file):
        source_file="%s/%04d%02d%02d%02d/psobs_posterior.txt.gz" % (sourcedir,
                         current.year,current.month,current.day,current.hour)
        target_file="%s/%04d%02d%02d%02d_psobs_posterior.txt.gz" % (
                         o_opdir,
                         current.year,current.month,current.day,current.hour)       
    copyfile(source_file,target_file)
    current=current+datetime.timedelta(hours=6)
