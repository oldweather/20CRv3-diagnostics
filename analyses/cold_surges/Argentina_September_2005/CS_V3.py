#!/usr/bin/env python

# South America plot
# MSLP and 850hPa temperature from 20CRv3

import math
import datetime
import numpy
import pandas

import iris
import iris.analysis

import matplotlib
from matplotlib.backends.backend_agg import \
             FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import cartopy
import cartopy.crs as ccrs

import Meteorographica as mg
import IRData.twcr as twcr

# Date to show
year=2005
month=9
day=12
hour=12
dte=datetime.datetime(year,month,day,hour)

# Landscape page
fig=Figure(figsize=(22,22/math.sqrt(2)),  # Width, Height (inches)
           dpi=100,
           facecolor=(0.88,0.88,0.88,1),
           edgecolor=None,
           linewidth=0.0,
           frameon=False,
           subplotpars=None,
           tight_layout=None)
canvas=FigureCanvas(fig)

# South America-centred projection
projection=ccrs.RotatedPole(pole_longitude=120, pole_latitude=125)
scale=25
extent=[scale*-1,scale,scale*-1*math.sqrt(2),scale*math.sqrt(2)]

# Two side-by-side plots
ax_2c=fig.add_axes([0.01,0.01,0.485,0.98],projection=projection)
ax_2c.set_axis_off()
ax_2c.set_extent(extent, crs=projection)
ax_3=fig.add_axes([0.505,0.01,0.485,0.98],projection=projection)
ax_3.set_axis_off()
ax_3.set_extent(extent, crs=projection)

# Background, grid and land for both
ax_2c.background_patch.set_facecolor((0.88,0.88,0.88,1))
ax_3.background_patch.set_facecolor((0.88,0.88,0.88,1))
mg.background.add_grid(ax_2c)
mg.background.add_grid(ax_3)
land_img_2c=ax_2c.background_img(name='GreyT', resolution='low')
land_img_3=ax_3.background_img(name='GreyT', resolution='low')

# Observations
obs=twcr.load_observations_fortime(dte,version='4.5.2')
obs=obs.loc[((obs['Latitude']<10) & 
                 (obs['Latitude']>-90)) &
              ((obs['Longitude']>270) & 
                 (obs['Longitude']<330))].copy()
mg.observations.plot(ax_2c,obs,radius=0.15)

# MSLP
prmsl=twcr.load('prmsl',dte,version='4.5.2')

# Contour spaghetti plot of MSLP ensemble
mg.pressure.plot(ax_2c,prmsl,scale=0.01,type='spaghetti',
                   resolution=0.25,
                   levels=numpy.arange(870,1050,10),
                   colors='blue',
                   label=False,
                   linewidths=0.1)

# Add the ensemble mean - with labels
prmsl_m=prmsl.collapsed('member', iris.analysis.MEAN)
mg.pressure.plot(ax_2c,prmsl_m,scale=0.01,
                   resolution=0.25,
                   levels=numpy.arange(870,1050,10),
                   colors='black',
                   label=True,
                   linewidths=2)

# MSLP label
mg.utils.plot_label(ax_2c,'MSLP',
                     facecolor=fig.get_facecolor(),
                     x_fraction=0.02,
                     horizontalalignment='left')

# T850 panel

T_cmap = matplotlib.colors.LinearSegmentedColormap('t_cmap',
                             {'red'  : ((0.0, 0.3, 0.3), 
                                        (0.5, 0.3, 0.3), 
                                        (1.0, 1.0, 1.0)), 
                              'green': ((0.0, 0.3, 0.3), 
                                        (0.5, 0.3, 0.3), 
                                        (1.0, 0.3, 0.3)), 
                              'blue' : ((0.0, 1.0, 1.0), 
                                        (0.5, 0.3, 0.3), 
                                        (1.0, 0.3, 0.3)), 
                              'alpha': ((0.0, 1.0, 1.0),
                                        (0.5, 1.0, 1.0),
                                        (1.0, 1.0, 1.0)) })


mg.observations.plot(ax_3,obs,radius=0.15)

t850=twcr.load('tmp',dte,level=850,version='4.5.2')

# Contour spaghetti plot of ensemble members
# Only use 56 members to match v2c
t850_r=t850.extract(iris.Constraint(member=list(range(0,56))))
lev=numpy.arange(265,295,5)
lev_f=(lev-numpy.min(lev))/float(numpy.max(lev)-numpy.min(lev))
mg.pressure.plot(ax_3,t850_r,scale=1,type='spaghetti',
                   resolution=0.25,
                   levels=lev,
                   colors=T_cmap(lev_f),
                   label=False,
                   linewidths=0.15)

# Add the ensemble mean - with labels
t850_m=t850.collapsed('member', iris.analysis.MEAN)
mg.pressure.plot(ax_3,t850_m,scale=1,
                   resolution=0.25,
                   levels=lev,
                   colors=T_cmap(lev_f),
                   label=True,
                   linewidths=2)

mg.utils.plot_label(ax_3,'Temperature at 850hPa',
                     facecolor=fig.get_facecolor(),
                     x_fraction=0.02,
                     horizontalalignment='left')

mg.utils.plot_label(ax_3,
              '%04d-%02d-%02d:%02d' % (year,month,day,hour),
              facecolor=fig.get_facecolor(),
              x_fraction=0.98,
              horizontalalignment='right')

# Output as png
fig.savefig('CS_V3_%04d%02d%02d%02d.png' % 
                                  (year,month,day,hour))
