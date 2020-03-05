#!/usr/bin/env python

# Compare pre-calculated stripes from 20CRv3 and scout 4.6.1
# Add axes and a grid.

import os
import numpy
import datetime
import pickle

import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

start=datetime.date(1926,1,1)
end=datetime.date(1935,12,31)

start_e=datetime.date(1930,10,1)
end_e=datetime.date(1931,9,30)

# Assemble the 4.6.1 sample
dts=[]
ndata_scout=None
current=start
while current<=end:
    try:
        sfile=("%s/20CR/version_4.6.1/analyses/Stripes_daily/TMP2m/"+
             "%04d%02d%02d.pkl") % (os.getenv('SCRATCH'),
                                    current.year,current.month,current.day)
        with open(sfile, "rb") as f:
           nddy  = pickle.load(f)
    except Exception:
        nddy=[numpy.ma.array(numpy.zeros((1,256)),mask=True)]
    if ndata_scout is None:
        ndata_scout = nddy[0]
    else:
        ndata_scout = numpy.ma.concatenate((ndata_scout,nddy[0]))

    dts.extend([current])
    current+=datetime.timedelta(days=1)

# Assemble the 20CR sample
ndata_20CR=None
current=start
while current<=end:
    sfile=("%s/20CR/version_3/analyses/Stripes_daily/TMP2m/"+
         "%04d%02d%02d.pkl") % (os.getenv('SCRATCH'),
                                current.year,current.month,current.day)
    with open(sfile, "rb") as f:
       nddy  = pickle.load(f)

    if ndata_20CR is None:
        ndata_20CR = nddy[0]
    else:
        ndata_20CR = numpy.ma.concatenate((ndata_20CR,nddy[0]))
    current+=datetime.timedelta(days=1)

# Assemble the difference sample
ndata_diff=None
current=start
while current<=end:
    try:
        sfile=("%s/20CR/version_3/analyses/Stripes_daily/461-TMP2m/"+
             "%04d%02d%02d.pkl") % (os.getenv('SCRATCH'),
                                    current.year,current.month,current.day)
        with open(sfile, "rb") as f:
           nddy  = pickle.load(f)
    except Exception:
        nddy=[numpy.ma.array(numpy.zeros((1,256)),mask=True)]

    if ndata_diff is None:
        ndata_diff = nddy[0]
    else:
        ndata_diff = numpy.ma.concatenate((ndata_diff,nddy[0]))
    current+=datetime.timedelta(days=1)

fig=Figure(figsize=(19.2,13),              # Width, Height (inches)
           dpi=100,
           facecolor=(0.5,0.5,0.5,1),
           edgecolor=None,
           linewidth=0.0,
           frameon=False,                
           subplotpars=None,
           tight_layout=None)
canvas=FigureCanvas(fig)
matplotlib.rc('image',aspect='auto')

def add_latline(ax,latitude):
    latl = (latitude+90)/180
    ax.add_line(Line2D([0.02,1],
                       [latl,latl],
                       linewidth=0.75,
                       color=(0.2,0.2,0.2,1),
                       zorder=200))
    ax.text(0.018,latl,
         "%d" % latitude,
         horizontalalignment='right',
         verticalalignment='center',
         color='black',
         size=14,
         clip_on=True,
         zorder=200)

# 4.6.1 at the top

# Add a textured grey background
s=(2000,600)
ax2 = fig.add_axes([0.02,0.68,0.98,0.32],facecolor='green')
ax2.set_axis_off() # Don't want surrounding x and y axis
nd2=numpy.random.rand(s[1],s[0])
clrs=[]
for shade in numpy.linspace(.42+.01,.36+.01):
    clrs.append((shade,shade,shade,1))
y = numpy.linspace(0,1,s[1])
x = numpy.linspace(0,1,s[0])
img = ax2.pcolormesh(x,y,nd2,
                        cmap=matplotlib.colors.ListedColormap(clrs),
                        alpha=1.0,
                        shading='gouraud',
                        zorder=10)

ndata_scout=numpy.transpose(ndata_scout)
s=ndata_scout.shape
ax = fig.add_axes([0.02,0.68,0.98,0.32],facecolor='black',
                  xlim=(0,1), # pcolorfast can't do dates
                  ylim=(1,0))
ax.set_axis_off()

y = numpy.linspace(0,1,s[0]+1)
x = numpy.linspace(0,1,s[1]+1)
img = ax.pcolorfast(x,y,numpy.cbrt(ndata_scout),
                        cmap='RdYlBu_r',
                        alpha=1.0,
                        vmin=-1.7,
                        vmax=1.7,
                        zorder=100)
# Add a latitude grid
axg = fig.add_axes([0.0,0.68,1,0.32],facecolor='green',
                   xlim=(0,1),
                   ylim=(0,1))
axg.set_axis_off()

for lat in [-60,-30,0,30,60]:
    add_latline(axg,lat)

# 20CRv3 in the middle

# Add a textured grey background
s=(2000,600)
ax2 = fig.add_axes([0.02,0.35,0.98,0.32],facecolor='green')
ax2.set_axis_off() # Don't want surrounding x and y axis
nd2=numpy.random.rand(s[1],s[0])
clrs=[]
for shade in numpy.linspace(.42+.01,.36+.01):
    clrs.append((shade,shade,shade,1))
y = numpy.linspace(0,1,s[1])
x = numpy.linspace(0,1,s[0])
img = ax2.pcolormesh(x,y,nd2,
                        cmap=matplotlib.colors.ListedColormap(clrs),
                        alpha=1.0,
                        shading='gouraud',
                        zorder=10)
# Plot the stripes
ndata_20CR=numpy.transpose(ndata_20CR)
s=ndata_20CR.shape
ax = fig.add_axes([0.02,0.35,0.98,0.32],facecolor='black',
                  xlim=(0,1), # pcolorfast can't do dates
                  ylim=(1,0))
ax.set_axis_off()

y = numpy.linspace(0,1,s[0]+1)
x = numpy.linspace(0,1,s[1]+1)
img = ax.pcolorfast(x,y,numpy.cbrt(ndata_20CR),
                        cmap='RdYlBu_r',
                        alpha=1.0,
                        vmin=-1.7,
                        vmax=1.7,
                        zorder=100)
# Add a latitude grid
axg = fig.add_axes([0.0,0.35,1.0,0.32],facecolor='green',
                   xlim=(0,1),
                   ylim=(0,1))
axg.set_axis_off()

for lat in [-60,-30,0,30,60]:
    add_latline(axg,lat)

# Difference at the bottom

# Add a textured grey background
s=(2000,600)
ax2 = fig.add_axes([0.02,0.02,0.98,0.32],facecolor='green')
ax2.set_axis_off() # Don't want surrounding x and y axis
nd2=numpy.random.rand(s[1],s[0])
clrs=[]
for shade in numpy.linspace(.42+.01,.36+.01):
    clrs.append((shade,shade,shade,1))
y = numpy.linspace(0,1,s[1])
x = numpy.linspace(0,1,s[0])
img = ax2.pcolormesh(x,y,nd2,
                        cmap=matplotlib.colors.ListedColormap(clrs),
                        alpha=1.0,
                        shading='gouraud',
                        zorder=10)

# Plot the stripes
ndata_diff=numpy.transpose(ndata_diff)
s=ndata_diff.shape
ax = fig.add_axes([0.02,0.02,0.98,0.32],facecolor='black',
                  xlim=(0,1), # pcolorfast can't do dates
                  ylim=(1,0))
ax.set_axis_off()

y = numpy.linspace(0,1,s[0]+1)
x = numpy.linspace(0,1,s[1]+1)
img = ax.pcolorfast(x,y,numpy.cbrt(ndata_diff),
                        cmap='RdYlBu_r',
                        alpha=1.0,
                        vmin=-1.7,
                        vmax=1.7,
                        zorder=100)
# Add a latitude grid
axg = fig.add_axes([0.0,0.02,1.0,0.32],facecolor='green',
                   xlim=(0,1),
                   ylim=(0,1))
axg.set_axis_off()

for lat in [-60,-30,0,30,60]:
    add_latline(axg,lat)

# Add a date grid
axg = fig.add_axes([0,0,1,1],facecolor='green',
                   xlim=(start,end),
                   ylim=(0,1))
axg.set_axis_off()

def add_dateline(ax,year):
    x = datetime.date(year,1,1)
    ax.add_line(Line2D([x,x], [0.02,1.0], 
                linewidth=0.75, 
                color=(0.2,0.2,0.2,1),
                       zorder=200))
    ax.text(x,0.01,
         "%04d" % year,
         horizontalalignment='center',
         verticalalignment='center',
         color='black',
         size=14,
         clip_on=True,
         zorder=200)

for year in range(1927,1936,1):
    add_dateline(axg,year)

fig.savefig('comparison_grid.png')
