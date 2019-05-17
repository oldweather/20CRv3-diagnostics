#!/usr/bin/env python

# Set up the figure and add the continents as background
# Overlay the observations at a point in time

import os
import datetime
import IRData.twcr as twcr
import Meteorographica as mg
import iris

import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import cartopy
import cartopy.crs as ccrs

version='4.5.1'

# Get the datetime to plot from commandline arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--year", help="Year",
                    type=int,required=True)
parser.add_argument("--month", help="Integer month",
                    type=int,required=True)
parser.add_argument("--day", help="Day of month",
                    type=int,required=True)
parser.add_argument("--hour", help="Time of day (0 to 23.99)",
                    type=float,required=True)
parser.add_argument("--opdir", help="Directory for output files",
                    default="%s/images/v3_obs/1902" % \
                                           os.getenv('SCRATCH'),
                    type=str,required=False)
args = parser.parse_args()
if not os.path.isdir(args.opdir):
    os.makedirs(args.opdir)

dte=datetime.datetime(args.year,args.month,args.day,
                      int(args.hour),int(args.hour%1*60))

# HD video size 1920x1080
aspect=16.0/9.0
fig=Figure(figsize=(10.8*aspect,10.8),  # Width, Height (inches)
           dpi=100,
           facecolor=(0.88,0.88,0.88,1),
           edgecolor=None,
           linewidth=0.0,
           frameon=False,
           subplotpars=None,
           tight_layout=None)
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
mg.observations.plot(ax,obs,radius=0.75,alpha=1.0,edgecolor='grey')

# Add a label showing the date
label="%04d-%02d-%02d:%02d" % (dte.year,dte.month,dte.day,dte.hour)
mg.utils.plot_label(ax,label,
                    facecolor=fig.get_facecolor())

# Render the figure as a png
# Output as png
fig.savefig('%s/Observations_%04d%02d%02d%02d%02d.png' % 
               (args.opdir,args.year,args.month,args.day,
                           int(args.hour),int(args.hour%1*60)))
