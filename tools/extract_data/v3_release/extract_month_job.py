#!/usr/bin/env python

# Run an xfer job to extract a month's V3 data to $SCRATCH

import tempfile
import argparse
import subprocess
import os

parser = argparse.ArgumentParser()
parser.add_argument("--startyear", help="Year run started",
                    type=int, required=True)
parser.add_argument("--year", help="Year to extract",
                    type=int, required=True)
parser.add_argument("--month", help="Month to extract",
                    type=int, required=True)
parser.add_argument("--version", help="Version to extract",
                    type=int,default=451)
args = parser.parse_args()

tfile=tempfile.NamedTemporaryFile(delete=False)
ldir=os.path.abspath(os.path.dirname(__file__))
tfile.write('#!/bin/bash -l\n')
tfile.write("#SBATCH --output=v3_extraction-%d-%d-%%j.out\n" %
                (args.year,args.month))
tfile.write('#SBATCH -M escori\n')
tfile.write('#SBATCH -q xfer\n')
tfile.write('#SBATCH -p regular\n')
tfile.write('#SBATCH -C knl\n')
tfile.write('#SBATCH -N 1\n')
tfile.write('#SBATCH -t 6:00:00\n')
tfile.write("#SBATCH -J V3ft%04d%02d\n" % (args.year,args.month))
tfile.write('#SBATCH -L SCRATCH\n')
tfile.write('module load python\n')
tfile.write('%s/month_from_tape.py --startyear=%d --year=%d --month=%d --version=%d\n' % 
                                  (ldir,args.startyear,args.year,args.month,args.version))
# Submit the conversion job
tfile.write('module unload esslurm; %s/conversion_job.py --startyear=%d --year=%d --month=%d --version=%d\n' % 
                                  (ldir,args.startyear,args.year,args.month,args.version))
tfile.close()

proc = subprocess.Popen('module load esslurm; sbatch %s' % tfile.name,shell=True)
(out, err) = proc.communicate()
if out is not None or err is not None:
    raise Exception("Failed to submit %s" % tfile.name)

os.remove(tfile.name)
#print tfile.name

