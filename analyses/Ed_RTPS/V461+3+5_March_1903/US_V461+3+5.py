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
month = 3
day = 25
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
extent = [
    scale * -2 / 3,
    scale * 2 / 3,
    scale * -1 * math.sqrt(2),
    scale * math.sqrt(2),
]

# Three side-by-side plots
ax_1 = fig.add_axes([0.01, 0.01, 0.315, 0.98], projection=projection)
ax_1.set_axis_off()
ax_1.set_extent(extent, crs=projection)
ax_5 = fig.add_axes([0.335, 0.01, 0.315, 0.98], projection=projection)
ax_5.set_axis_off()
ax_5.set_extent(extent, crs=projection)
ax_3 = fig.add_axes([0.675, 0.01, 0.315, 0.98], projection=projection)
ax_3.set_axis_off()
ax_3.set_extent(extent, crs=projection)

# Background, grid and land for all three
ax_1.patch.set_facecolor((0.88, 0.88, 0.88, 1))
ax_3.patch.set_facecolor((0.88, 0.88, 0.88, 1))
ax_5.patch.set_facecolor((0.88, 0.88, 0.88, 1))
mg.background.add_grid(ax_1)
mg.background.add_grid(ax_3)
mg.background.add_grid(ax_5)
land_img_1 = ax_1.background_img(name="GreyT", resolution="low")
land_img_3 = ax_3.background_img(name="GreyT", resolution="low")
land_img_5 = ax_5.background_img(name="GreyT", resolution="low")

# Add the observations from 461
obs = twcr.load_observations_fortime(dte, version="4.6.1")
mg.observations.plot(ax_1, obs, radius=0.15)

# load the v3 pressures
prmsl = twcr.load("PRMSL", dte, version="4.6.1")

# Contour spaghetti plot of ensemble members
mg.pressure.plot(
    ax_1,
    prmsl,
    scale=0.01,
    type="spread",
    resolution=0.05,
    levels=numpy.arange(870, 1050, 10),
)

# label
mg.utils.plot_label(
    ax_1,
    "RTPS 0.9",
    facecolor=fig.get_facecolor(),
    x_fraction=0.02,
    horizontalalignment="left",
)

# Add the observations from 4.6.5
obs = twcr.load_observations_fortime(dte, version="4.6.5")
mg.observations.plot(ax_5, obs, radius=0.15)

# load the 4.6.5 pressures
prmsl = twcr.load("PRMSL", dte, version="4.6.5")

# Contour spaghetti plot of ensemble members
mg.pressure.plot(
    ax_5,
    prmsl,
    scale=0.01,
    type="spread",
    resolution=0.05,
    levels=numpy.arange(870, 1050, 10),
)

mg.utils.plot_label(
    ax_5,
    "RTPS 0.5",
    facecolor=fig.get_facecolor(),
    x_fraction=0.02,
    horizontalalignment="left",
)

# Add the observations from 4.6.3
obs = twcr.load_observations_fortime(dte, version="4.6.3")
mg.observations.plot(ax_3, obs, radius=0.15)

# load the 4.6.3 pressures
prmsl = twcr.load("PRMSL", dte, version="4.6.3")

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
    "RTPS 0.3",
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
fig.savefig("V461+3+5_Ulysses_storm_%04d%02d%02d%02d.png" % (year, month, day, hour))
