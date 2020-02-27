#!/usr/bin/env python

# 20CRv3 time-series: Monthly average, regional average.
#  Each ensemble member as a seperate line.

# Uses pre-calculated time-series.

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

start=datetime.datetime(1806,1,1,0,0)
end=datetime.datetime(2015,12,31,23,59)

ylim = (-250,250)

dts=[]
ndata=None
for year in range(start.year,end.year+1,1):
    sfile="%s/20CR/version_3/analyses/Stripes/HGT500_ts/%04d.pkl" % \
                                           (os.getenv('SCRATCH'),year)
    with open(sfile, "rb") as f:
       (ndyr,dtyr)  = pickle.load(f)

    dts.extend([dtyr[0:11]])
    if ndata is None:
        ndata = ndyr[0:11,:]
    else:
        ndata = numpy.ma.concatenate((ndata,ndyr[0:11,:]))

# Plot the resulting array as a set of line graphs
fig=Figure(figsize=(19.2,6),              # Width, Height (inches)
           dpi=300,
           facecolor=(0.5,0.5,0.5,1),
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

# Plot the lines
ax = fig.add_axes([0.05,0.05,0.93,0.93],
                  xlim=((start-datetime.timedelta(days=1)),
                        (end+datetime.timedelta(days=1))),
                  ylim=ylim)
ax.set_ylabel('Z500 anomaly')

#x = [a.timestamp() for a in dts]
for m in range(80):
    ax.add_line(Line2D(dts, 
                       ndata[:,m], 
                       linewidth=0.5, 
                       color=(0,0,1,1),
                       alpha=0.05,
                       zorder=200))
fig.savefig('HGT500_ts.png')

