#!/usr/bin/env python

# UK region weather plot 
# Collect reanalysis comparison data for
# Every DWR ob in a month

import os
import sys
import datetime
import pandas
import iris
import pickle
import multiprocessing
import time

import IRData.twcr as twcr
import IRData.cera20c as cera20c

import DWR

# Get the period to compare from commandline arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--start", help="Start: yyyymm(dd(hh))",
                    type=str,required=True)
parser.add_argument("--end", help="End: yyyymm(dd(hh))",
                    type=str,required=True)
parser.add_argument("--reanalysis", help="20cr2c | 20cr3 | cera",
                    type=str,required=True)
parser.add_argument("--skip", help="names of stations to omit",
                    type=str, action='append',default=[])
parser.add_argument("--npar", help="Number of parallel tasks",
                    type=int,default=1)

args = parser.parse_args()

start=datetime.datetime(int(args.start[0:4]),
                        int(args.start[4:6]),
                        1,0)
if len(args.start) >= 8:
    start=start+datetime.timedelta(days=int(args.start[6:8]))
if len(args.start) >= 10:
    start=start+datetime.timedelta(hours=int(args.start[8:10]))

end=datetime.datetime(int(args.end[0:4]),
                      int(args.end[4:6]),
                      1,0)
if len(args.end) >= 8:
    end=end+datetime.timedelta(days=int(args.end[6:8]))
if len(args.end) >= 10:
    end=end+datetime.timedelta(hours=int(args.end[8:10]))

current=start

# Load all the DWR obs
obs=DWR.load_observations('prmsl',start,end)
# Skip specified DWR stations
if len(args.skip)>0:
    obs=obs[~obs['name'].isin(args.skip)]

# Set output directory
opdir=("%s/images/DWR/reanalysis_comparison_%s" % 
                (os.getenv('SCRATCH'),args.reanalysis))
if not os.path.isdir(opdir):
    os.makedirs(opdir)

# Get a list of all the times where there is at least 1 observation.
ob_times=obs['dtm'].unique()
# At each such time, get the reanalysis ensemble at all the
#   stations reporting at that time.

# Get the reanalysis ensemble for all observations at a time and 
#  pickle it to disc
def at_time(ob_time):
    ensembles=[]
    observations=[]
    ob_time=pandas.to_datetime(ob_time)
    opfile="%s/%04d-%02d-%02d:%02d:%02d.pkl" % (opdir,
        ob_time.year,ob_time.month,ob_time.day,
        ob_time.hour,ob_time.minute)
    if os.path.isfile(opfile): 
        time.sleep(0.1) # returning too fast breaks multiprocessing
        return # Done already
    print ob_time
    try:
        if args.reanalysis=='20cr3':
            prmsl=twcr.load('prmsl',ob_time,version='4.5.1')
        elif args.reanalysis=='20cr2c':
            prmsl=twcr.load('prmsl',ob_time,version='2c')
        elif args.reanalysis=='cera':
            prmsl=cera20c.load('prmsl',ob_time)
        else:
            print "Unsupported reanalysis %s" % args.reanalysis
            sys.exit(1)
    except Exception as e:
        print "Failed to load data for %s" % str(ob_time)
        return  

    prmsl.data=prmsl.data/100.0 # to hPa
    interpolator = iris.analysis.Linear().interpolator(prmsl, 
                                   ['latitude', 'longitude'])
    obs_current=obs[obs['dtm']==ob_time]
    for ob in obs_current.itertuples():
        ensemble=interpolator([ob.latitude,ob.longitude])
        ensembles.append([ensemble.data])
        observations.append(ob.value) 

    afile = open(opfile, 'wb')
    pickle.dump({'ensembles': ensembles,
                 'observations':observations}, afile)
    afile.close()
        
pool = multiprocessing.Pool(processes=args.npar)
# Use map_async and over-longtimeout, instead of just map, to make ctrl^c work.
pool.map_async(at_time,ob_times).get(9999999)
