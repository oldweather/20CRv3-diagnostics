#!/usr/bin/env python

# 20CRv3 time-series: 3-hourly data, point values.
#  Each ensemble member as a seperate line.

# Uses pre-calculated time-series.

import os
import iris
import numpy
import datetime
from calendar import monthrange
import pickle

import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--startyear", help="Start Year", type=int, default=1903, required=False
)
parser.add_argument(
    "--startmonth", help="Start Month", type=int, default=2, required=False
)
parser.add_argument("--startday", help="Start Day", type=int, default=1, required=False)
parser.add_argument(
    "--starthour", help="Start Hour", type=int, default=6, required=False
)
parser.add_argument(
    "--endyear", help="End Year", type=int, default=1903, required=False
)
parser.add_argument("--endmonth", help="End Month", type=int, default=2, required=False)
parser.add_argument("--endday", help="End Day", type=int, default=28, required=False)
parser.add_argument("--endhour", help="End Hour", type=int, default=18, required=False)
parser.add_argument("--lat", help="Latitude", type=float, required=True)
parser.add_argument("--lon", help="Longitude (0-360)", type=float, required=True)
parser.add_argument("--var", help="Variable to plot", type=str, required=True)
parser.add_argument(
    "--version",
    help="20CR version ('3' or e.g. '4.6.5')",
    default="3",
    type=str,
    required=True,
)
parser.add_argument(
    "--comparison",
    help="20CR version ('3' or e.g. '4.6.5')",
    default=None,
    type=str,
    required=False,
)
parser.add_argument(
    "--comparison2",
    help="20CR version ('3' or e.g. '4.6.5')",
    default=None,
    type=str,
    required=False,
)
parser.add_argument(
    "--comparison3",
    help="20CR version ('3' or e.g. '4.6.5')",
    default=None,
    type=str,
    required=False,
)
parser.add_argument(
    "--ymin", help="Y-axis minimum", type=float, default=None, required=False
)
parser.add_argument(
    "--ymax", help="Y-axis maximum", type=float, default=None, required=False
)
parser.add_argument(
    "--yscale", help="Y-axis scale factor", type=float, default=1.0, required=False
)
args = parser.parse_args()
start = datetime.datetime(
    args.startyear, args.startmonth, args.startday, args.starthour
)
end = datetime.datetime(args.endyear, args.endmonth, args.endday, args.endhour)


def fromversion(version, year_offset=0):
    dts = []
    ndata = None
    lstart = datetime.datetime(
        start.year + year_offset, start.month, start.day, start.hour
    ) - datetime.timedelta(days=30)
    lend = datetime.datetime(
        end.year + year_offset, end.month, end.day, end.hour
    ) + datetime.timedelta(days=30)
    current = lstart
    while current <= lend:
        opf = (
            "%s/20CRv3_point_data/version_%s/%s/%04d/%02d/%02d/"
            + "%02d_00_%+07.2f_%+06.2f.pkl"
        ) % (
            os.getenv("SCRATCH"),
            version,
            args.var,
            current.year,
            current.month,
            current.day,
            current.hour,
            args.lon,
            args.lat,
        )
        # Skip leap days to simplify inter-year comparisons
        if not (current.month == 2 and current.day == 29):
            if os.path.exists(opf):
                with open(opf, "rb") as f:
                    nddy = pickle.load(f)
                if ndata is None:
                    ndata = numpy.reshape(nddy, [1, 80])
                else:
                    ndata = numpy.ma.concatenate((ndata, numpy.reshape(nddy, [1, 80])))
                dts.append(
                    datetime.datetime(
                        current.year - year_offset,
                        current.month,
                        current.day,
                        current.hour,
                    )
                )
        current += datetime.timedelta(hours=3)
    return (ndata, dts)


# Calculate the ensemble average
def ensm(values):
    return numpy.mean(values, axis=1)


# Calculate a running mean
def movingaverage(dates, values, window):
    weights = numpy.repeat(1.0, window) / window
    sma = numpy.convolve(values, weights, "valid")
    # same processing on the dates array
    epoch = dates[0]
    dates = numpy.array([(d - epoch).total_seconds() for d in dates])
    dms = numpy.convolve(dates, weights, "valid").tolist()
    dms = [epoch + datetime.timedelta(seconds=d) for d in dms]
    return (dms, sma)


# Get the 3-hourly data
(ndata, dts) = fromversion(args.version, year_offset=0)
if args.ymin is None:
    args.ymin = numpy.amin(ndata) * args.yscale
if args.ymax is None:
    args.ymax = numpy.amax(ndata) * args.yscale

# Plot the resulting array as a set of line graphs
fig = Figure(
    figsize=(19.2, 6),  # Width, Height (inches)
    dpi=300,
    facecolor=(0.5, 0.5, 0.5, 1),
    edgecolor=None,
    linewidth=0.0,
    frameon=False,
    subplotpars=None,
    tight_layout=None,
)
canvas = FigureCanvas(fig)
font = {"family": "sans-serif", "sans-serif": "Arial", "weight": "normal", "size": 16}
matplotlib.rc("font", **font)
axb = fig.add_axes([0, 0, 1, 1])

ax = fig.add_axes(
    [0.06, 0.06, 0.93, 0.92],
    xlim=((start - datetime.timedelta(days=1)), (end + datetime.timedelta(days=1))),
    ylim=(args.ymin, args.ymax),
)
if args.yscale == 1:
    ax.set_ylabel(args.var)
else:
    ax.set_ylabel("%s (*%g)" % (args.var, args.yscale))


# 3-hourly, all ensemble members
for m in range(80):
    ax.add_line(
        Line2D(
            dts,
            ndata[:, m] * args.yscale,
            linewidth=0.1,
            color=(0, 0, 0, 1),
            alpha=1.0,
            zorder=200,
        )
    )

# Add the ensemble mean
(dtsrm, rmem) = (dts, ensm(ndata) * args.yscale)
ax.add_line(
    Line2D(
        dtsrm,
        rmem,
        linewidth=2.0,
        color=(0, 0, 0, 1),
        alpha=0,
        zorder=250,
    )
)

if args.comparison is not None:
    # Add the comparison dataset
    (nd2, dts2) = fromversion(args.comparison)
    for m in range(80):
        ax.add_line(
            Line2D(
                dts2,
                nd2[:, m] * args.yscale,
                linewidth=0.1,
                color=(1, 0, 0, 1),
                alpha=1.0,
                zorder=300,
            )
        )
    (dtsrm, rmem) = (dts2, ensm(nd2) * args.yscale)
    ax.add_line(
        Line2D(
            dtsrm,
            rmem,
            linewidth=2.0,
            color=(1, 0, 0, 1),
            alpha=0,
            zorder=350,
        )
    )

if args.comparison2 is not None:
    # Add the ensemble mean for the second comparison dataset
    (nd2, dts2) = fromversion(args.comparison2)
    for m in range(80):
        ax.add_line(
            Line2D(
                dts2,
                nd2[:, m] * args.yscale,
                linewidth=0.1,
                color=(0, 0, 1, 1),
                alpha=1.0,
                zorder=400,
            )
        )
    (dtsrm, rmem) = (dts2, ensm(nd2) * args.yscale)
    ax.add_line(
        Line2D(
            dtsrm,
            rmem,
            linewidth=2.0,
            color=(0, 0, 1, 1),
            alpha=0,
            zorder=450,
        )
    )

if args.comparison3 is not None:
    # Add the ensemble mean for the third comparison dataset
    (nd2, dts2) = fromversion(args.comparison3)
    (dtsrm, rmem) = (dts2, ensm(nd2) * args.yscale)
    ax.add_line(
        Line2D(
            dtsrm,
            rmem,
            linewidth=2.0,
            color=(1, 0.5, 0.5, 1),
            alpha=0,
            zorder=280,
        )
    )

fig.savefig("%s.png" % args.var)
