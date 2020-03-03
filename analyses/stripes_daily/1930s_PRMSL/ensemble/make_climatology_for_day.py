#!/usr/bin/env python

# Make a climatology for a single day over the specified period

import os
import iris
import numpy
import datetime
import pickle

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--month", help="Month",
                    type=int,required=True)
parser.add_argument("--day", help="Day",
                    type=int,required=True)
parser.add_argument("--startyear", help="Start Year",
                    type=int,required=False,default=1926)
parser.add_argument("--endyear", help="End Year",
                    type=int,required=False,default=1935)
parser.add_argument("--opdir", help="Directory for output files",
                    default="%s/20CR/version_3/analyses/daily/PRMSL" % \
                                           os.getenv('SCRATCH'),
                    type=str,required=False)
args = parser.parse_args()
opdir = "%s/clim_%04d-%04d" % (args.opdir,args.startyear,args.endyear)
if not os.path.isdir(opdir):
    os.makedirs(opdir)

# Fix dask SPICE bug
import dask
dask.config.set(scheduler='single-threaded')

from get_sample import load_daily

y=[]
for year in range(args.startyear,args.endyear+1):
   m=load_daily(year,args.month,args.day)
   m=m.collapsed('member',iris.analysis.MEAN)
   y.append(m)
y=iris.cube.CubeList(y).merge_cube()
y=y.collapsed('time',iris.analysis.MEAN)

cspf = "%s/%02d%02d.pkl" % (opdir,args.month,args.day)
pickle.dump(y,open(cspf,'wb'))
