#!/usr/bin/env python

# Extract surface variables from a month's V3 output
#  and convert to netCDF

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
tfile.write('#!/bin/bash\n')
tfile.write("#SBATCH --output=v3_conversion-%d-%d-%%j.out\n" %
                (args.year,args.month))
tfile.write('#SBATCH -p regular\n')
tfile.write('#SBATCH -C knl\n')
tfile.write('#SBATCH -N 1\n')
tfile.write('#SBATCH -t 5:30:00\n')
tfile.write("#SBATCH -J V3co%04d%02d\n" % (args.year,args.month))
tfile.write('#SBATCH -L SCRATCH\n\n')
tfile.write('module load ncar\n')
tfile.write('module load nco\n')
tfile.write('module load python\n\n')
tfile.write('mkdir -p %s/20CRv3.final/version_%d.%d.%d/%02d/%02d\n' % 
                                                 (os.getenv('SCRATCH'),int(args.version/100),
                                                  int((args.version%100)/10),int(args.version%10),
                                                               args.year,args.month))
tfile.write('export OMP_NUM_THREADS=10\n\n')
ldir=os.path.abspath(os.path.dirname(__file__))
tfile.write('%s/extract_anl_var.py --startyear=%d --year=%d --month=%d --version=%d --var=prmsl &\n' % 
                                                         (ldir,args.startyear,args.year,args.month,args.version))
tfile.write('%s/extract_anl_var.py --startyear=%d --year=%d --month=%d --version=%d --var=air.2m &\n' % 
                                                         (ldir,args.startyear,args.year,args.month,args.version))
tfile.write('%s/extract_anl_var.py --startyear=%d --year=%d --month=%d --version=%d --var=uwnd.10m &\n' % 
                                                         (ldir,args.startyear,args.year,args.month,args.version))
tfile.write('%s/extract_anl_var.py --startyear=%d --year=%d --month=%d --version=%d --var=vwnd.10m &\n' % 
                                                         (ldir,args.startyear,args.year,args.month,args.version))
tfile.write('%s/extract_anl_var.py --startyear=%d --year=%d --month=%d --version=%d --var=air.sfc &\n' % 
                                                         (ldir,args.startyear,args.year,args.month,args.version))
tfile.write('%s/extract_anl_var.py --startyear=%d --year=%d --month=%d --version=%d --var=icec &\n' % 
                                                         (ldir,args.startyear,args.year,args.month,args.version))
tfile.write('%s/extract_anl_var.py --startyear=%d --year=%d --month=%d --version=%d --var=hgt --level=850 &\n' % 
                                                         (ldir,args.startyear,args.year,args.month,args.version))
tfile.write('%s/extract_anl_var.py --startyear=%d --year=%d --month=%d --version=%d --var=tmp --level=850 &\n' % 
                                                         (ldir,args.startyear,args.year,args.month,args.version))
tfile.write('%s/extract_anl_var.py --startyear=%d --year=%d --month=%d --version=%d --var=spfh --level=850 &\n' % 
                                                         (ldir,args.startyear,args.year,args.month,args.version))
tfile.write('%s/extract_anl_var.py --startyear=%d --year=%d --month=%d --version=%d --var=uwnd --level=850 &\n' % 
                                                         (ldir,args.startyear,args.year,args.month,args.version))
tfile.write('%s/extract_anl_var.py --startyear=%d --year=%d --month=%d --version=%d --var=vwnd --level=850 &\n' % 
                                                         (ldir,args.startyear,args.year,args.month,args.version))
tfile.write('%s/extract_fg_var.py --startyear=%d --year=%d --month=%d --version=%d --var=prate &\n' % 
                                                         (ldir,args.startyear,args.year,args.month,args.version))
tfile.write('%s/extract_obs.py --startyear=%d --year=%d --month=%d --version=%d &\n' % 
                                                         (ldir,args.startyear,args.year,args.month,args.version))
tfile.write('wait\n')
tfile.write('%s/cleanup.py --startyear=%d --year=%d --month=%d --version=%d\n' % 
                                                         (ldir,args.startyear,args.year,args.month,args.version))
tfile.close()

proc = subprocess.Popen('sbatch %s' % tfile.name,shell=True)
(out, err) = proc.communicate()
if out is not None or err is not None:
    raise Exception("Failed to submit %s" % tfile.name)
os.remove(tfile.name)

	 
