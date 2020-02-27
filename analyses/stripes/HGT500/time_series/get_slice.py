#!/usr/bin/env python

# 20CRv3 stripes.
# Monthly, mean over lat:lon range, 
#  sampling the ensemble.

# Get the sample for a specified year

import os
import iris
import numpy
import datetime
import pickle

import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--year", help="Year",
                    type=int,required=True)
parser.add_argument("--min_lat", help="Min latitude",
                    type=float,required=False,default=-90.0)
parser.add_argument("--max_lat", help="Max latitude",
                    type=float,required=False,default=90.0)
parser.add_argument("--min_lon", help="Min longitude",
                    type=float,required=False,default=-180.0)
parser.add_argument("--max_lon", help="Max longitude",
                    type=float,required=False,default=360.0)
parser.add_argument("--opdir", help="Directory for output files",
                    default="%s/20CR/version_3/analyses/Stripes/HGT500_ts" % \
                                           os.getenv('SCRATCH'),
                    type=str,required=False)
args = parser.parse_args()
if not os.path.isdir(args.opdir):
    os.makedirs(args.opdir)

# Fix dask SPICE bug
import dask
dask.config.set(scheduler='single-threaded')

start=datetime.datetime(args.year,1,1,0,0)
end=datetime.datetime(args.year,12,31,23,59)

from get_sample import get_sample

cpkl="%s/20CR/version_3/monthly_means/HGT500.climatology.1961-90.pkl" % os.getenv('SCRATCH')
climatology=pickle.load(open(cpkl,'rb'))

dts=[]
ndata=None
for year in range(start.year,end.year+1,1):
    ey = min(year+1,end.year)
    (ndyr,dtyr) = get_sample(max_lat=args.max_lat,
                                  min_lat=args.min_lat,
                                  max_lon=args.max_lon,
                                  min_lon=args.min_lon,
                                  start=datetime.datetime(year,1,1,0,0),
                                  end=datetime.datetime(year,12,31,23,59),
                                  climatology=climatology,
                                  new_grid=climatology[0])
    dts.extend(dtyr)
    if ndata is None:
        ndata = ndyr
    else:
        ndata = numpy.ma.concatenate((ndata,ndyr))

cspf = "%s/%04d.pkl" % (args.opdir,args.year)
pickle.dump((ndata,dts),open(cspf,'wb'))
   
