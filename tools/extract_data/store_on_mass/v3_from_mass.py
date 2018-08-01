#!/usr/bin/env python

# Retrieve archived 20CRv3 data from MASS

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

# Disc data dir
ddir="%s/20CR/version_%s/" % (os.environ['SCRATCH'],args.version)
if not os.path.isdir(ddir):
    os.makedirs(ddir)

# Retrieve the observations
def retrieve_obs(year,month,version,variable):
    # Are they on disc
    ofiles=glob.glob("%s/observations/%04d/%04d%02d*.txt" %
                           (ddir,year,year,month))
    if len(ofiles)>100:
        return         # Already on disc

    proc = subprocess.Popen("moo ls %s/observations.tgz" % moose_dir,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True)
    (out, err) = proc.communicate()
    if len(err)!=0:
        if variable=='observations':
            raise StandardError("Obs file not on mass %s/observations.tgz" 
                                 % moose_dir)
        return

    # Retrieve ob file from MASS
    proc = subprocess.Popen("moo get %s %s/observations.tgz %s/observations/%04d" % 
                                              (otarf,moose_dir,ddir,year),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               shell=True)
    (out, err) = proc.communicate()
    if len(err)!=0:
        print err
        raise StandardError("Failed to retrieve observations %s" % otarf)
    # Pack the month's obs into a single file
    otarf=("%s/observations/%04d/observations.tgz" % 
                           (ddir,year))
    proc = subprocess.Popen(
            "cd %s ; tar xzf %s observations/%04d/observations.tgz" 
               % (ddir,otarf,year),
               stdout=subprocess.PIPE,
               stderr=subprocess.PIPE,
               shell=True)
    (out, err) = proc.communicate()
    if len(err)!=0:
        print err
        raise StandardError("Failed to untar observations")

    # Clean up
    os.remove(otarf)

# Retrieve a variable file
def retrieve_variable(year,month,version,variable):
    vf="%s/%04d/%02d/%s.nc" % (ddir,year,month,variable)
    if os.path.isfile(vf):
        return  # already on disc
    
    proc = subprocess.Popen("moo get %s/%s.nc %s" % 
                             (moose_dir,variable,os.path.dirname(vf)),
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=True)
    (out, err) = proc.communicate()
    if len(err) !=0:
        print err
        raise StandardError("Failed to retrieve %s/%s.nc" % 
                             (moose_dir,variable))


if args.variable=='all':
    proc = subprocess.Popen("moo ls %s" % moose_dir,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True)
    (out, err) = proc.communicate()
    if len(err)!=0: 
        print err
        raise StandardError("Can't find any data in %s" % moose_dir)

    if len(re.findall('.*\.tgz',out))>0:
        retrieve_obs(args.year,args.month,args.version,args.variable)

    for var in re.findall('.*\.nc',out):
        variable=os.path.splitext(os.path.basename(var))[0]
        retrieve_variable(args.year,args.month,args.version,variable)
elif args.variable=='observations':
    retrieve_obs(args.year,args.month,args.version,args.variable)
else:
    retrieve_variable(args.year,args.month,args.version,args.variable)