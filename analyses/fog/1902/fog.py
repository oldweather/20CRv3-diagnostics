#!/usr/bin/env python

# Set up the figure and add the continents as background
# Overlay the ensemble mean pressure and a fog uncertainty layer

import datetime
import IRData.twcr as twcr
import Meteorographica as mg
import iris

import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import cartopy
import cartopy.crs as ccrs

import numpy

# Pick a time to plot
dte=datetime.datetime(1902,8,12,6)
version='4.5.1'

# Define the figure (page size, background color, resolution, ...
aspect=16/9.0
fig=Figure(figsize=(22,22/aspect),              # Width, Height (inches)
           dpi=100,
           facecolor=(0.88,0.88,0.88,1),
           edgecolor=None,
           linewidth=0.0,
           frameon=False,                # Don't draw a frame
           subplotpars=None,
           tight_layout=None)
# Attach a canvas
canvas=FigureCanvas(fig)

# All mg plots use Rotated Pole, in this case just use the standard
#  pole location.
projection=ccrs.RotatedPole(pole_longitude=180.0, pole_latitude=90.0)

# Define an axes to contain the plot. In this case our axes covers
#  the whole figure
ax = fig.add_axes([0,0,1,1],projection=projection)
ax.set_axis_off() # Don't want surrounding x and y axis
# Set the axes background colour
ax.background_patch.set_facecolor((0.88,0.88,0.88,1))

# Lat and lon range (in rotated-pole coordinates) for plot
extent=[-180.0,180.0,-90.0,90.0]
ax.set_extent(extent, crs=projection)
# Lat:Lon aspect does not match the plot aspect, ignore this and
#  fill the figure with the plot.
matplotlib.rc('image',aspect='auto')

# Draw a lat:lon grid
mg.background.add_grid(ax,
                       sep_major=5,
                       sep_minor=2.5,
                       color=(0,0.3,0,0.2))


# Add the land
land_img=ax.background_img(name='GreyT', resolution='low')

# Load the pressures
prmsl=twcr.load('prmsl',dte,version=version)
# Load the standard deviations
sd=twcr.load('prmsl',dte,version='2c',type='standard.deviation')
# regrid to v3 resolution
sd=sd.regrid(prmsl,iris.analysis.Linear())


# Plot the ensemble mean - with labels
prmsl_m=prmsl.collapsed('member', iris.analysis.STD_DEV)
#prmsl_m=prmsl_m/sd
mg.pressure.plot(ax,prmsl_m,scale=1,
                   resolution=0.25,
                   levels=numpy.arange(0,600,50),
                   colors='blue',
                   label=True,
                   linewidths=1,
                   zorder=200)


# Add a label showing the date
label="%04d-%02d-%02d:%02d" % (dte.year,dte.month,dte.day,dte.hour)
mg.utils.plot_label(ax,label,
                    facecolor=fig.get_facecolor(),zorder=500)

# Render the figure as a png
fig.savefig('fog.png')
