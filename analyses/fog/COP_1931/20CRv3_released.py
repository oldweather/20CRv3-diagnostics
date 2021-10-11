#!/usr/bin/env python

# Wind (and fog) in COP26 colour scheme

import os
import IRData.twcr as twcr
import datetime
import pickle

import iris
import numpy as np
import math

import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

from pandas import qcut

# COP colour scheme
COP_white = (1.0, 1.0, 1.0)
COP_blue = (55 / 255, 52 / 255, 139 / 255)
COP_green = (140 / 255, 219 / 255, 114 / 255)

# Fix dask SPICE bug
import dask

dask.config.set(scheduler="single-threaded")

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--year", help="Year", type=int, required=True)
parser.add_argument("--month", help="Integer month", type=int, required=True)
parser.add_argument("--day", help="Day of month", type=int, required=True)
parser.add_argument(
    "--hour", help="Time of day (0 to 23.99)", type=float, required=True
)
parser.add_argument(
    "--pole_latitude",
    help="Latitude of projection pole",
    default=90,
    type=float,
    required=False,
)
parser.add_argument(
    "--pole_longitude",
    help="Longitude of projection pole",
    default=180,
    type=float,
    required=False,
)
parser.add_argument(
    "--npg_longitude",
    help="Longitude of view centre",
    default=0,
    type=float,
    required=False,
)
parser.add_argument(
    "--zoom",
    help="Scale factor for viewport (1=global)",
    default=1,
    type=float,
    required=False,
)
parser.add_argument(
    "--opdir",
    help="Directory for output files",
    default="%s/images/20CRv3_COP" % os.getenv("SCRATCH"),
    type=str,
    required=False,
)
parser.add_argument(
    "--zfile",
    help="Noise pickle file name",
    default="%s/images/20CRv3_COP/z.pkl" % os.getenv("SCRATCH"),
    type=str,
    required=False,
)

args = parser.parse_args()
if not os.path.isdir(args.opdir):
    os.makedirs(args.opdir)


dte = datetime.datetime(
    args.year, args.month, args.day, int(args.hour), int(args.hour % 1 * 60)
)


u10m = twcr.load("UGRD10m", dte, version="3", member=1)
v10m = twcr.load("VGRD10m", dte, version="3", member=1)
# prmsl all members for spread
prmsl = twcr.load("PRMSL", dte, version="3", member=None)
prmsl = prmsl.collapsed("member", iris.analysis.STD_DEV)

mask = iris.load_cube(
    "%s/fixed_fields/land_mask/opfc_global_2019.nc" % os.getenv("DATADIR")
)

# Load the climatological prmsl stdev from v2c
prevt = datetime.datetime(
    args.year, args.month, args.day, int(args.hour) - int(args.hour) % 6
)
prevcsd = iris.load_cube(
    "/data/users/hadpb/20CR/version_3.4.1/standard.deviation/prmsl.nc",
    iris.Constraint(
        time=iris.time.PartialDateTime(
            year=1981, month=prevt.month, day=prevt.day, hour=prevt.hour
        )
    ),
)
nextt = prevt + datetime.timedelta(hours=6)
nextcsd = iris.load_cube(
    "/data/users/hadpb/20CR/version_3.4.1/standard.deviation/prmsl.nc",
    iris.Constraint(
        time=iris.time.PartialDateTime(
            year=1981, month=nextt.month, day=nextt.day, hour=nextt.hour
        )
    ),
)
w = (dte - prevt).total_seconds() / (nextt - prevt).total_seconds()
prevcsd.data = prevcsd.data * (1 - w) + nextcsd.data * w
coord_s = iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)
prevcsd.coord("latitude").coord_system = coord_s
prevcsd.coord("longitude").coord_system = coord_s


# Define the figure (page size, background color, resolution, ...
fig = Figure(
    figsize=(19.2, 10.8),  # Width, Height (inches)
    dpi=100,
    facecolor=(0.5, 0.5, 0.5, 1),
    edgecolor=None,
    linewidth=0.0,
    frameon=False,  # Don't draw a frame
    subplotpars=None,
    tight_layout=None,
)
fig.set_frameon(False)
# Attach a canvas
canvas = FigureCanvas(fig)

# Projection for plotting
cs = iris.coord_systems.RotatedGeogCS(
    args.pole_latitude, args.pole_longitude, args.npg_longitude
)


def plot_cube(resolution, xmin, xmax, ymin, ymax):

    lat_values = np.arange(ymin, ymax + resolution, resolution)
    latitude = iris.coords.DimCoord(
        lat_values, standard_name="latitude", units="degrees_north", coord_system=cs
    )
    lon_values = np.arange(xmin, xmax + resolution, resolution)
    longitude = iris.coords.DimCoord(
        lon_values, standard_name="longitude", units="degrees_east", coord_system=cs
    )
    dummy_data = np.zeros((len(lat_values), len(lon_values)))
    plot_cube = iris.cube.Cube(
        dummy_data, dim_coords_and_dims=[(latitude, 0), (longitude, 1)]
    )
    return plot_cube


# Make the wind noise
def wind_field(
    uw, vw, zf, sequence=None, iterations=50, mfraction=0.5, epsilon=0.003, sscale=1
):
    # Random field as the source of the distortions
    z = pickle.load(open(zf, "rb"))
    offset = z.copy()
    if sequence is not None:
        fod = offset.data.flatten()
        fod = (np.arange(len(fod)) * 13 + sequence) % int(iterations * mfraction)
        offset.data = fod.reshape(z.data.shape)
    else:
        offset.data *= 0
    z = z.regrid(uw, iris.analysis.Nearest())
    offset = offset.regrid(uw, iris.analysis.Nearest())
    (width, height) = z.data.shape
    # Each point in this field has an index location (i,j)
    #  and a real (x,y) position
    xmin = np.min(uw.coords()[0].points)
    xmax = np.max(uw.coords()[0].points)
    ymin = np.min(uw.coords()[1].points)
    ymax = np.max(uw.coords()[1].points)
    # Convert between index and real positions
    def i_to_x(i):
        return xmin + (i / width) * (xmax - xmin)

    def j_to_y(j):
        return ymin + (j / height) * (ymax - ymin)

    def x_to_i(x):
        return np.minimum(
            width - 1, np.maximum(0, np.floor((x - xmin) / (xmax - xmin) * (width - 1)))
        ).astype(int)

    def y_to_j(y):
        return np.minimum(
            height - 1,
            np.maximum(0, np.floor((y - ymin) / (ymax - ymin) * (height - 1))),
        ).astype(int)

    i, j = np.mgrid[0:width, 0:height]
    x = i_to_x(i)
    y = j_to_y(j)
    # Result is a distorted version of the random field
    result = z.copy()
    # Repeatedly, move the x,y points according to the vector field
    #  and update result with the random field at their locations
    for k in range(iterations):
        x += epsilon * vw.data[i, j]
        x[x > xmax] = xmax
        x[x < xmin] = xmin
        y += epsilon * uw.data[i, j]
        y[y > ymax] = y[y > ymax] - ymax + ymin
        y[y < ymin] = y[y < ymin] - ymin + ymax
        i = x_to_i(x)
        j = y_to_j(y)
        update = z.data.copy()
        update[k < offset.data] = 0
        update[k > (offset.data + int(iterations * (1.0 - mfraction)))] = 0
        result.data[i, j] = np.maximum(result.data[i, j], update)
    result.data -= z.data  # Delete the fixed starting dot
    return result


wind_pc = plot_cube(
    0.2, -180 / args.zoom, 180 / args.zoom, -90 / args.zoom, 90 / args.zoom
)
rw = iris.analysis.cartography.rotate_winds(u10m, v10m, cs)
u10m = rw[0].regrid(wind_pc, iris.analysis.Linear())
v10m = rw[1].regrid(wind_pc, iris.analysis.Linear())
seq = (dte - datetime.datetime(2000, 1, 1)).total_seconds() / 3600
# wind_noise_field=wind_field(u10m,v10m,args.zfile,sequence=int(seq*5),epsilon=0.03)
wind_noise_field = wind_field(
    u10m,
    v10m,
    args.zfile,
    sequence=int(seq * 2),
    epsilon=0.025,
    iterations=50,
    mfraction=0.75,
)

# Define an axes to contain the plot. In this case our axes covers
#  the whole figure
ax = fig.add_axes([0, 0, 1, 1])
ax.set_axis_off()  # Don't want surrounding x and y axis

# Lat and lon range (in rotated-pole coordinates) for plot
xlim = (-180 / args.zoom, 180 / args.zoom)
ylim = (-90 / args.zoom, 90 / args.zoom)
ax.set_xlim(xlim[0], xlim[1])
ax.set_ylim(ylim[0], ylim[1])
ax.set_aspect("auto")

# Background
ax.add_patch(
    Rectangle(
        (xlim[0], ylim[0]),
        xlim[1] - xlim[0],
        ylim[1] - ylim[0],
        facecolor=COP_blue,
        fill=True,
        zorder=1,
    )
)

# Plot the land mask
mask_pc = plot_cube(
    0.05, -180 / args.zoom, 180 / args.zoom, -90 / args.zoom, 90 / args.zoom
)
mask = mask.regrid(mask_pc, iris.analysis.Linear())
lats = mask.coord("latitude").points
lons = mask.coord("longitude").points
mask_img = ax.pcolorfast(
    lons,
    lats,
    mask.data,
    cmap=matplotlib.colors.ListedColormap(
        (
            (COP_green[0], COP_green[1], COP_green[2], 0),
            (COP_green[0], COP_green[1], COP_green[2], 1),
        )
    ),
    vmin=0,
    vmax=1,
    alpha=1.0,
    zorder=20,
)

# Plot the fog of ignorance
prmsl = prmsl.regrid(mask_pc, iris.analysis.Linear())
prevcsd = prevcsd.regrid(mask_pc, iris.analysis.Linear())
prmsl.data = np.minimum(1, prmsl.data / prevcsd.data)
cols = []


def fog_map(x):
    return 1 / (1 + np.exp((x - 0.5) * -10))


for ci in range(100):
    cols.append([COP_white[0], COP_white[1], COP_white[2], fog_map(ci / 100)])

fog_img = ax.pcolorfast(
    lons,
    lats,
    prmsl.data * np.random.uniform(0.75, 1.0, size=prmsl.data.shape),
    cmap=matplotlib.colors.ListedColormap(cols),
    alpha=0.95,
    zorder=300,
)


# Plot the wind vectors
wnf = wind_noise_field.regrid(mask_pc, iris.analysis.Linear())
t2m_img = ax.pcolorfast(
    lons,
    lats,
    wnf.data * (1.0 - prmsl.data / 1.5),
    cmap=matplotlib.colors.ListedColormap(cols),
    alpha=1.0,
    zorder=100,
)


# Label with the date
ax.text(
    180 / args.zoom - (360 / args.zoom) * 0.009,
    90 / args.zoom - (180 / args.zoom) * 0.016,
    "%04d-%02d-%02d" % (args.year, args.month, args.day),
    horizontalalignment="right",
    verticalalignment="top",
    color=COP_white,
    bbox=dict(facecolor=COP_blue, edgecolor=COP_white, boxstyle="round", pad=0.5),
    size=14,
    clip_on=True,
    zorder=500,
)

# Render the figure as a png
fig.savefig(
    "%s/%04d%02d%02d%02d%02d.png"
    % (
        args.opdir,
        args.year,
        args.month,
        args.day,
        int(args.hour),
        int(args.hour % 1 * 60),
    )
)
