#!/usr/bin/env python

# 20CRv3 stripes.
# Daily, resolved in latitude, averaging in longitude, 
#  ensemble sample.

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

start=datetime.date(1926,1,1)
end=datetime.date(1935,12,31)

dts=[]
ndata=None
current=start
while current<=end:
    sfile=("%s/20CR/version_3/analyses/Stripes_daily/PRMSL/"+
         "%04d%02d%02d.pkl") % (os.getenv('SCRATCH'),
                                current.year,current.month,current.day)
    with open(sfile, "rb") as f:
       nddy  = pickle.load(f)

    if ndata is None:
        ndata = nddy[0]
    else:
        ndata = numpy.ma.concatenate((ndata,nddy[0]))

    dts.extend([current])
    current+=datetime.timedelta(days=1)

# Plot the resulting array as a 2d colourmap
fig=Figure(figsize=(19.2,6),              # Width, Height (inches)
           dpi=300,
           facecolor=(0.5,0.5,0.5,1),
           edgecolor=None,
           linewidth=0.0,
           frameon=False,                
           subplotpars=None,
           tight_layout=None)
canvas=FigureCanvas(fig)
matplotlib.rc('image',aspect='auto')


# Add a textured grey background
s=(2000,600)
ax2 = fig.add_axes([0.02,0.05,0.98,0.95],facecolor='green')
ax2.set_axis_off() 
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
ndata=numpy.transpose(ndata)
s=ndata.shape
ax = fig.add_axes([0.02,0.05,0.98,0.95],facecolor='black',
                  xlim=(0,1), # pcolorfast can't do dates
                  ylim=(1,0))
ax.set_axis_off()

y = numpy.linspace(0,1,s[0]+1)
x = numpy.linspace(0,1,s[1]+1)
img = ax.pcolorfast(x,y,numpy.cbrt(ndata),
                        cmap='RdYlBu_r',
                        alpha=1.0,
                        vmin=-13,
                        vmax=13,
                        zorder=100)

# Add a latitude grid
axg = fig.add_axes([0.0,0.05,1,0.95],facecolor='green',
                   xlim=(0,1),
                   ylim=(0,1))
axg.set_axis_off()

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

for lat in (-60,-30,0,30,60):
    add_latline(axg,lat)

# Add a date grid
axg = fig.add_axes([0.02,0,0.98,1],facecolor='green',
                   xlim=(start,end),
                   ylim=(0,1))
axg.set_axis_off()

def add_dateline(ax,year):
    x = datetime.date(year,1,1)
    ax.add_line(Line2D([x,x], [0.04,1.0], 
                linewidth=0.75, 
                color=(0.2,0.2,0.2,1),
                       zorder=200))
    ax.text(x,0.024,
         "%04d" % year,
         horizontalalignment='center',
         verticalalignment='center',
         color='black',
         size=14,
         clip_on=True,
         zorder=200)


for year in range(1927,1936,1):
    add_dateline(axg,year)

fig.savefig('PRMSL.png')

