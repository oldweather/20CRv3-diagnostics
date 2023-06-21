#!/usr/bin/env python

# UK region weather plot
# Compare pressures from 20CRV3 and Wind assimilation run 5.7.6

import os
import sys
import math
import datetime
import numpy as np

import iris
import iris.analysis
import iris.coord_systems
from iris.analysis.cartography import rotate_pole

iris.FUTURE.datum_support = True

import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.colors import LinearSegmentedColormap

import warnings

warnings.filterwarnings("ignore", message=".*coordinate is contiguous.*")

import v3_load
import scout_load

# Date to show
year = 1915
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

# Plot cube with selected projecion
coord_plot = iris.coord_systems.RotatedGeogCS(
    grid_north_pole_longitude=180,
    grid_north_pole_latitude=90,
    north_pole_grid_longitude=45,
)
scale = 90 / math.sqrt(2)
extent = [scale * -1, scale, scale * -1 * math.sqrt(2), scale * math.sqrt(2)]
resolution = 0.25
x_coord = iris.coords.DimCoord(
    np.arange(extent[0], extent[1], resolution),
    standard_name="longitude",
    units="degrees",
    coord_system=coord_plot,
)
x_coord.guess_bounds()
y_coord = iris.coords.DimCoord(
    np.arange(extent[2], extent[3], resolution),
    standard_name="latitude",
    units="degrees",
    coord_system=coord_plot,
)
y_coord.guess_bounds()
dummy_data = np.zeros((len(y_coord.points), len(x_coord.points)))
sCube = iris.cube.Cube(dummy_data, dim_coords_and_dims=[(x_coord, 1), (y_coord, 0)])
lats = sCube.coord("latitude").points
lons = sCube.coord("longitude").points

# Also want a land mask for plotting:
lm_plot = iris.load_cube(
    "%s/fixed_fields/land_mask/opfc_global_2019.nc" % os.getenv("DATADIR")
)
lm_plot = lm_plot.regrid(sCube, iris.analysis.Linear())

# Background
ax_global = fig.add_axes([0, 0, 1, 1], facecolor="white")

# Left axes for v3 plot
ax_3 = fig.add_axes([0.01, 0.01, 0.485, 0.98])
ax_3.set_axis_off()
ax_3.set_xlim(extent[0], extent[1])
ax_3.set_ylim(extent[2], extent[3])

# Background and land mask
land_img = ax_3.pcolorfast(
    lons, lats, lm_plot.data, cmap="Greys", alpha=0.3, vmax=1.2, vmin=-0.5, zorder=10
)

# Pressure observations as points
obs = v3_load.load_observations_fortime(dte, version="3")
rp = rotate_pole(
    obs["Longitude"].values,
    obs["Latitude"].values,
    coord_plot.grid_north_pole_longitude,
    coord_plot.grid_north_pole_latitude,
)
new_longitude = rp[0] + coord_plot.north_pole_grid_longitude
new_longitude[new_longitude > 180] -= 360
new_latitude = rp[1]

# Plot each ob as a circle
for i in range(0, len(new_longitude)):
    ax_3.add_patch(
        matplotlib.patches.Circle(
            (new_longitude[i], new_latitude[i]),
            radius=0.35,
            facecolor="yellow",
            edgecolor="black",
            alpha=1.0,
            zorder=10,
        )
    )

# Spaghetti plot of pressures
prmsl = v3_load.load("PRMSL", dte, version="3")
prmsl = prmsl.regrid(sCube, iris.analysis.Linear())
for e in range(80):
    CS = ax_3.contour(
        lons,
        lats,
        prmsl.data[e, :, :] / 100,
        colors="blue",
        linewidths=0.1,
        linestyles="solid",
        alpha=1.0,
        levels=np.arange(870, 1030, 10),
        zorder=20,
    )
# Make field of ensemble spread
v3_spread = prmsl.collapsed("member", iris.analysis.STD_DEV)

# Label
ax_3.text(
    extent[0] + scale / 20,
    extent[2] + scale / 15,
    "V3",
    horizontalalignment="left",
    verticalalignment="bottom",
    color="black",
    bbox=dict(
        facecolor=(0.8, 0.8, 0.8, 0.8), edgecolor="black", boxstyle="round", pad=0.5
    ),
    size=16,
    clip_on=True,
    zorder=40,
)


# Right axes for scout plot
ax_scout = fig.add_axes([0.505, 0.01, 0.485, 0.98])
ax_scout.set_axis_off()
ax_scout.set_xlim(extent[0], extent[1])
ax_scout.set_ylim(extent[2], extent[3])

# Background and land mask
land_img = ax_scout.pcolorfast(
    lons, lats, lm_plot.data, cmap="Greys", alpha=0.3, vmax=1.2, vmin=-0.5, zorder=10
)

# Pressure observations as points
obs = scout_load.load_observations_fortime(dte, version="5.7.6")
rp = rotate_pole(
    obs["Longitude"].values,
    obs["Latitude"].values,
    coord_plot.grid_north_pole_longitude,
    coord_plot.grid_north_pole_latitude,
)
new_longitude = rp[0] + coord_plot.north_pole_grid_longitude
new_longitude[new_longitude > 180] -= 360
new_latitude = rp[1]

# Plot each ob as a circle
for i in range(0, len(new_longitude)):
    ax_scout.add_patch(
        matplotlib.patches.Circle(
            (new_longitude[i], new_latitude[i]),
            radius=0.35,
            facecolor="yellow",
            edgecolor="black",
            alpha=1.0,
            zorder=10,
        )
    )


prmsl = scout_load.load("prmsl", dte, version="5.7.6")
prmsl = prmsl.regrid(sCube, iris.analysis.Linear())
for e in range(80):
    CS = ax_scout.contour(
        lons,
        lats,
        prmsl.data[e, :, :] / 100,
        colors="blue",
        linewidths=0.1,
        linestyles="solid",
        alpha=1.0,
        levels=np.arange(870, 1030, 10),
        zorder=20,
    )

# Make field of ensemble spread
scout_spread = prmsl.collapsed("member", iris.analysis.STD_DEV)

# Label
ax_scout.text(
    extent[0] + scale / 20,
    extent[2] + scale / 15,
    "5.7.6",
    horizontalalignment="left",
    verticalalignment="bottom",
    color="black",
    bbox=dict(
        facecolor=(0.8, 0.8, 0.8, 0.8), edgecolor="black", boxstyle="round", pad=0.5
    ),
    size=16,
    clip_on=True,
    zorder=40,
)

# Make colormap for glow of discovery
cdict = {
    "red": [[0.0, 1.0, 1.0], [1.0, 1.0, 1.0]],
    "green": [[0.0, 1.0, 1.0], [1.0, 1.0, 1.0]],
    "blue": [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]],
    "alpha": [[0.0, 1.0, 1.0], [1.0, 0.0, 0.0]],
}
glow_cmp = LinearSegmentedColormap("glow_cmp", segmentdata=cdict, N=100)
# Mark areas where v3 is better
sratio = v3_spread / scout_spread
glow_img = ax_3.pcolorfast(
    lons, lats, sratio.data, cmap=glow_cmp, vmax=1, vmin=0.25, zorder=50
)
# Mark areas where scout is better
sratio = scout_spread / v3_spread
glow_img = ax_scout.pcolorfast(
    lons, lats, sratio.data, cmap=glow_cmp, vmax=1, vmin=0.25, zorder=50
)


# Output as png
fig.savefig("V3v576_%04d%02d%02d%02d.png" % (year, month, day, hour))
