#!/usr/bin/env python

# Scatter plot of reanalysis spread v reanalysis error

import os
import pickle
import datetime

import matplotlib
from matplotlib.backends.backend_agg import \
                 FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import DWR_plots

# Get the period to compare from commandline arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--start", help="Start: yyyymm(dd(hh))",
                    type=str,required=True)
parser.add_argument("--end", help="End: yyyymm(dd(hh))",
                    type=str,required=True)
parser.add_argument("--reanalysis", help="20cr2c | 20cr3 | cera",
                    type=str,required=True)
parser.add_argument("--nbins", help="no. of data bins",
                    type=int,default=20)

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

# load the pre-prepared data
ddir=("%s/images/DWR/reanalysis_comparison_%s" % 
                (os.getenv('SCRATCH'),args.reanalysis))
cdata={'ensembles':[],'observations':[]}
dfiles=os.listdir(ddir)
for dfl in dfiles:
   fdate=datetime.datetime(int(dfl[0:4]),int(dfl[5:7]),
                           int(dfl[8:10]),int(dfl[11:13]),
                           int(dfl[14:16]))
   if fdate<start or fdate >= end: continue
   d_file = open("%s/%s" % (ddir,dfl), 'rb')
   dpoint = pickle.load(d_file)
   d_file.close()
   cdata['ensembles']=cdata['ensembles']+dpoint['ensembles']
   cdata['observations']=cdata['observations']+dpoint['observations']

# Landscape page
fig=Figure(figsize=(11,11),  # Width, Height (inches)
           dpi=100,
           facecolor=(0.88,0.88,0.88,1),
           edgecolor=None,
           linewidth=0.0,
           frameon=False,
           subplotpars=None,
           tight_layout=None)
canvas=FigureCanvas(fig)
font = {'family' : 'sans-serif',
        'sans-serif' : 'Arial',
        'weight' : 'normal',
        'size'   : 16}
matplotlib.rc('font', **font)

# Fill the frame with an axes
ax=fig.add_axes([0.08,0.08,0.89,0.89])

DWR_plots.plot_eve(ax,cdata,nbins=args.nbins)

# Output as png
fig.savefig('E_v_E_%04d-%02d-%02d_to_%04d-%02d-%02d_%s.png' %
            (start.year,start.month,start.day,
             end.year,end.month,end.day,
             args.reanalysis))

