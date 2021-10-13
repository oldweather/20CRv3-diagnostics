#!/usr/bin/env python

# Make a fixed noise field for wind-map plots.

import os
import iris
import numpy as np
import random
import pickle

import os

import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--resolution",
    help="Resolution for plot grid",
    default=0.3,
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
    "--opfile",
    help="Output (pickle) file name",
    default="%s/images/COP_time_skips/z.pkl" % os.getenv("SCRATCH"),
    type=str,
    required=False,
)
args = parser.parse_args()
if not os.path.isdir(os.path.dirname(args.opfile)):
    os.makedirs(os.path.dirname(args.opfile))


# Nominal projection
cs = iris.coord_systems.RotatedGeogCS(90, 180, 0)


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


z = plot_cube(
    args.resolution, -180 / args.zoom, 180 / args.zoom, -90 / args.zoom, 90 / args.zoom
)
(width, height) = z.data.shape
for i in range(0, width, 5):
    for j in range(0, height, 5):
        xi = i + random.randint(-1, 1)
        if xi >= width:
            xi -= width
        if xi < 0:
            xi += width
        yi = j + random.randint(-1, 1)
        if yi >= height:
            yi -= height
        if yi < 0:
            yi += height
        z.data[xi, yi] = 1
        # if(yi<(height-1)): z.data[xi,yi+1]=1
        # if(yi>0): z.data[xi,yi-1]=1
        # if(xi<(width-1)): z.data[xi+1,yi]=1
        # if(xi>0): z.data[xi-1,yi]=1

pickle.dump(z, open(args.opfile, "wb"))
