#!/usr/bin/env python

# Scatter plot of reanalysis spread v reanalysis error

import os
import pickle
import datetime
import numpy

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

d_range=[960,1045]

# x-axis
ax.set_xlim(d_range)
ax.set_xlabel('Observed MSLP (hPa)')
# y-axis
ax.set_ylim(d_range)
ax.set_ylabel('Ensemble MSLP (hPa)')

# Background 1-to-1 line
ax.add_line(matplotlib.lines.Line2D(
            xdata=[d_range],
            ydata=[d_range],
            linestyle='solid',
            linewidth=1,
            color=(0.5,0.5,0.5,1),
            zorder=1))

# Plot the ensembles
jitter=numpy.linspace(-0.5,0.5,len(cdata['ensembles'][0][0]))
for idx in range(len(cdata['observations'])):
    obs_ens=[cdata['observations'][idx]]*len(cdata['ensembles'][idx][0])
    ax.scatter(obs_ens+jitter,
               cdata['ensembles'][idx][0],
               s=5,
               marker='.',
               alpha=0.25,
               linewidths=0.01,
               c='blue',
               edgecolors='blue')

# Output as png
fig.savefig('Scatter_%04d-%02d-%02d_to_%04d-%02d-%02d_%s.png' %
            (start.year,start.month,start.day,
             end.year,end.month,end.day,
             args.reanalysis))

