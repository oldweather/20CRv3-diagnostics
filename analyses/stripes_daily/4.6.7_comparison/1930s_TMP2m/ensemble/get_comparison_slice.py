#!/usr/bin/env python

# Scout_461-20CRv3 stripes.
# Daily, resolved in latitude, averaging in longitude, 
#  sampling the ensemble.

# Get the sample for a specified day

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
parser.add_argument("--month", help="Month",
                    type=int,required=True)
parser.add_argument("--day", help="Day",
                    type=int,required=True)
parser.add_argument("--startyear", help="Start Year",
                    type=int,required=False,default=1926)
parser.add_argument("--endyear", help="End Year",
                    type=int,required=False,default=1935)
parser.add_argument("--opdir", help="Directory for output files",
                    default="%s/20CR/version_3/analyses/Stripes_daily/467-TMP2m" % \
                                           os.getenv('SCRATCH'),
                    type=str,required=False)
args = parser.parse_args()
if not os.path.isdir(args.opdir):
    os.makedirs(args.opdir)

# Fix dask SPICE bug
import dask
dask.config.set(scheduler='single-threaded')

from get_comparison_sample import get_sample_cube

cday=args.day
if args.month==2 and args.day==29: cday=28
cpkl="%s/20CR/version_3/analyses/daily/TMP2m/clim_%04d-%04d/%02d%02d.pkl" % (
           os.getenv('SCRATCH'),args.startyear,args.endyear,args.month,cday)
climatology_20CR=pickle.load(open(cpkl,'rb'))
coord_s=iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)
climatology_20CR.coord('latitude').coord_system=coord_s
climatology_20CR.coord('longitude').coord_system=coord_s

ndata=get_sample_cube(args.year,args.month,args.day,
                      climatology_20CR,
                      climatology_20CR)
dts=datetime.datetime(args.year,args.month,args.day,12)

cspf = "%s/%04d%02d%02d.pkl" % (args.opdir,args.year,args.month,args.day)
pickle.dump((ndata,dts),open(cspf,'wb'))
   

