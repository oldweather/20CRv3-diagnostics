#!/usr/bin/env python

# Archive downloaded 20CRv3 data in MASS

import sys
import os
import subprocess
import os.path
import glob

# What to store
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--year", help="Year",
                    type=int,required=True)
parser.add_argument("--month", help="Integer month",
                    type=int,required=True)
parser.add_argument("--version", help="Version, e.g. '4.5.1'",
                    type=str,required=False,
                    default='4.5.1')
parser.add_argument("--variable", 
                    help="Variable name ('prmsl','observations,...)",
                    type=str,required=False,
                    default='all')
parser.add_argument("--user", help="MASS user name",
                    type=str,required=False,
                    default='philip.brohan')
args = parser.parse_args()

# Base location for storage
mbase="moose:/adhoc/users/%s/20CRV3/" % args.user
moose_dir=("%s/version_%s/%04d/%02d" %
                (mbase,args.version,args.year,args.month))
# Make the moose directory
proc = subprocess.Popen("moo mkdir -p %s" % moose_dir,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        shell=True)
# If the directory already exists, this will throw an error
#  otherwise it will create the directory
(out, err) = proc.communicate()

# Disc data dir
ddir="%s/20CR/version_%s/" % (os.environ['SCRATCH'],args.version)

# Archive the observations
def archive_obs(year,month,version,variable):
    proc = subprocess.Popen("moo ls %s/observations.tgz" % moose_dir,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True)
    (out, err) = proc.communicate()
    if len(err)==0: return()  # Already archived

    # Are there any observations to archive?
    ofiles=glob.glob("%s/observations/%04d/%04d%02d*.txt" %
                           (ddir,year,year,month))
    if len(ofiles)==0:  # No obs on disc
        if variable=='observations':
            raise StandardError("No obs on disc for %04d-%02d %s" %
                                                (year,month,version))
        return()

    # Pack the month's obs into a single file
    otarf=("%s/observations/%04d/observations.tgz" % 
                           (ddir,year))
    proc = subprocess.Popen(
            "cd %s ; tar czf %s observations/%04d/%04d%02d*.txt" 
               % (ddir,otarf,year,year,month),
               stdout=subprocess.PIPE,
               stderr=subprocess.PIPE,
               shell=True)
    (out, err) = proc.communicate()
    if len(err)!=0:
        print err
        raise StandardError("Failed to tar observations")

    # Stow the ob file on MASS
    proc = subprocess.Popen("moo put %s %s/observations.tgz" % 
                                              (otarf,moose_dir),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               shell=True)
    (out, err) = proc.communicate()
    if len(err)!=0:
        print err
        raise StandardError("Failed to archive observations %s" % otarf)

    # Clean up
    os.remove(otarf)

# Archive a variable file
def archive_variable(year,month,version,variable):
    proc = subprocess.Popen("moo ls %s/%s.nc" % (moose_dir,variable),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True)
    (out, err) = proc.communicate()
    if len(err)==0: return()  # Already archived
    vf="%s/%04d/%02d/%s.nc" % (ddir,year,month,variable)
    if not os.path.isfile(vf):
        raise StandardError("No data file %s" % vf)
    proc = subprocess.Popen("moo put %s %s/%s.nc" % 
                             (vf,moose_dir,variable),
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=True)
    (out, err) = proc.communicate()
    if len(err) !=0:
        print err
        raise StandardError("Failed to archive %s" % vf)


if args.variable=='all':
    vars=glob.glob("%s/%04d/%02d/*.nc" % (ddir,args.year,args.month))
    for var in vars:
        variable=os.path.splitext(os.path.basename(var))[0]
        archive_variable(args.year,args.month,args.version,variable)
    archive_obs(args.year,args.month,args.version,args.variable)
elif args.variable=='observations':
    archive_obs(args.year,args.month,args.version,args.variable)
else:
    archive_variable(args.year,args.month,args.version,args.variable)
