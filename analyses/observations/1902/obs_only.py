#!/usr/bin/env python

# Set up the figure and add the continents as background
# Overlay the observations at a point in time

import datetime
import IRData.twcr as twcr
import Meteorographica as mg
import iris

import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import cartopy
import cartopy.crs as ccrs

import pkg_resources
import gzip
import pickle

# Pick a time to plot
dte=datetime.datetime(2005,9,12,6)
version='4.5.2'

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

# Load the observations for the selected date
obs=twcr.load_observations_fortime(dte,version=version)

# Plot the observations
mg.observations.plot(ax,obs,radius=0.75,alpha=1.0)

# Add a label showing the date
label="%04d-%02d-%02d:%02d" % (dte.year,dte.month,dte.day,dte.hour)
mg.utils.plot_label(ax,label,
                    facecolor=fig.get_facecolor())

# Render the figure as a png
fig.savefig('observations.png')
