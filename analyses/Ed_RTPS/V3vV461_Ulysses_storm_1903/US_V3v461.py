#!/usr/bin/env python

# UK region weather plot
# Compare pressures from 20CRV3 and 20CRV2c

import math
import datetime
import numpy
import pandas

import iris
import iris.analysis

import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import cartopy
import cartopy.crs as ccrs

import Meteorographica as mg
import IRData.twcr as twcr

# Date to show
year = 1903
month = 2
day = 27
hour = 6
dte = datetime.datetime(year, month, day, hour)

# Landscape page
fig = Figure(
    figsize=(22, 22 / math.sqrt(2)),  # Width, Height (inches)
    dpi=100,
    facecolor=(0.88, 0.88, 0.88, 1),
    edgecolor=None,
    linewidth=0.0,
    frameon=False,
    subplotpars=None,
    tight_layout=None,
)
canvas = FigureCanvas(fig)
axb = fig.add_axes([0, 0, 1, 1])

# UK-centred projection
projection = ccrs.RotatedPole(pole_longitude=180, pole_latitude=35)
scale = 15
extent = [scale * -1, scale, scale * -1 * math.sqrt(2), scale * math.sqrt(2)]

# Two side-by-side plots
ax_2c = fig.add_axes([0.01, 0.01, 0.485, 0.98], projection=projection)
ax_2c.set_axis_off()
ax_2c.set_extent(extent, crs=projection)
ax_3 = fig.add_axes([0.505, 0.01, 0.485, 0.98], projection=projection)
ax_3.set_axis_off()
ax_3.set_extent(extent, crs=projection)

# Background, grid and land for both
ax_2c.patch.set_facecolor((0.88, 0.88, 0.88, 1))
ax_3.patch.set_facecolor((0.88, 0.88, 0.88, 1))
mg.background.add_grid(ax_2c)
mg.background.add_grid(ax_3)
land_img_2c = ax_2c.background_img(name="GreyT", resolution="low")
land_img_3 = ax_3.background_img(name="GreyT", resolution="low")

# Add the observations from v3
obs = twcr.load_observations_fortime(dte, version="3")
mg.observations.plot(ax_2c, obs, radius=0.15)

# load the v3 pressures
prmsl = twcr.load("PRMSL", dte, version="3")

# Contour spaghetti plot of ensemble members
mg.pressure.plot(
    ax_2c,
    prmsl,
    scale=0.01,
    type="spread",
    resolution=0.05,
    levels=numpy.arange(870, 1050, 10),
)

# V3 label
mg.utils.plot_label(
    ax_2c,
    "20CR v3",
    facecolor=fig.get_facecolor(),
    x_fraction=0.02,
    horizontalalignment="left",
)

# V3 panel

# Add the observations from 4.6.1
obs = twcr.load_observations_fortime(dte, version="4.6.1")
mg.observations.plot(ax_3, obs, radius=0.15)

# load the 4.6.1 pressures
prmsl = twcr.load("PRMSL", dte, version="4.6.1")

# Contour spaghetti plot of ensemble members
mg.pressure.plot(
    ax_3,
    prmsl,
    scale=0.01,
    type="spread",
    resolution=0.05,
    levels=numpy.arange(870, 1050, 10),
)

mg.utils.plot_label(
    ax_3,
    "20CR 4.6.1",
    facecolor=fig.get_facecolor(),
    x_fraction=0.02,
    horizontalalignment="left",
)

mg.utils.plot_label(
    ax_3,
    "%04d-%02d-%02d:%02d" % (year, month, day, hour),
    facecolor=fig.get_facecolor(),
    x_fraction=0.98,
    horizontalalignment="right",
)

# Output as png
fig.savefig("V3v461_Ulysses_storm_%04d%02d%02d%02d.png" % (year, month, day, hour))
