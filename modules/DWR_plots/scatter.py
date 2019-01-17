# (C) British Crown Copyright 2017, Met Office
#
# This code is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This code is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#

# Plot station pressure and reanalysis ensemble for each station

import iris
import DWR
import numpy
import collections
import matplotlib

def plot_scatter(ax,field,dwr_obs,dte,**kwargs):
    """Make a mslp contour plot with DWR observations

    Args:
        ax (:`cartopy.axes`): Axes to hold the plot
        field (:obj:`iris.Cube.cube`): Reanalysis mslp ensemble
        dwr_obs (:obj:`pandas.DataFrame`): DWR observations.
        extent (:obj:`list`) Plot extent (lon.min,lon.max,lat.min,lat.max)
        xlabel (:obj:`str`): 'x-axis title'

    Kwargs:
        pressure_range (:obj:`list`): (min,max) pressure for scatterplot, default [945,1045].
        xlabel (:obj:`str`): x-axis label for scatter plot, default 'MSLP (hPa)'.
        scatter_point_size (:obj:`float`): Size of ensemble dots in scatter plot (pts), default 25.
        scatter_alpha (:obj:`float`): Alpha transparency of ensemble dots in scatter plot (pts), default 0.5.
        stations (:obj:`list`): Names (DWR format) of stations to be included, default is stations in dwr_obs.
        station_latlon (:obj:`dict`): Latitiudes and Longitudes of stations to be included, default is taken from dwr_obs.

    |
    """

    # Set keyword argument defaults
    kwargs.setdefault('pressure_range',[945,1045])
    kwargs.setdefault('xlabel','MSLP (hPa)')
    kwargs.setdefault('scatter_point_size',25)
    kwargs.setdefault('scatter_alpha',0.5)
    kwargs.setdefault('stations',list(collections.OrderedDict.fromkeys(
                                      dwr_obs.loc[:,'name']).keys()))
    if 'station_latlon' not in kwargs:
        latlon={}
        for station in kwargs.get('stations'):
           latlon[station]=DWR.get_station_location(dwr_obs,station)
        kwargs['station_latlon']=latlon

    # x-axis
    ax.set_xlim(kwargs.get('pressure_range'))
    ax.set_xlabel(kwargs.get('xlabel'))
 
    # y-axis
    ax.set_ylim([1,len( kwargs.get('stations'))+1])
    y_locations=[x+0.5 for x in range(1,len( kwargs.get('stations'))+1)]
    ax.yaxis.set_major_locator(
                  matplotlib.ticker.FixedLocator(y_locations))
    ax.yaxis.set_major_formatter(
                  matplotlib.ticker.FixedFormatter(
                      [DWR.pretty_name(s) for s in  kwargs.get('stations')]))
    
    # Custom grid spacing
    for y in range(0,len(kwargs.get('stations'))):
        ax.add_line(matplotlib.lines.Line2D(
                xdata=kwargs.get('pressure_range'),
                ydata=(y+1.5,y+1.5),
                linestyle='solid',
                linewidth=0.2,
                color=(0.5,0.5,0.5,1),
                zorder=0))

    # Plot the station pressures
    interpolated={}
    for station in kwargs.get('stations'):
        try:
            interpolated[station]=DWR.at_station_and_time(
                                              dwr_obs,station,dte)
        except Exception:
            interpolated[station]=None
    for y in range(0,len(kwargs.get('stations'))):
        station=kwargs.get('stations')[y]
        if interpolated[station] is None:
            continue
        mslp=interpolated[station]
        ax.add_line(matplotlib.lines.Line2D(
                xdata=(mslp,mslp), ydata=(y+1.25,y+1.75),
                linestyle='solid',
                linewidth=4,
                color=(1,0,0,1),
                zorder=1))

    # for each station, plot the reanalysis ensemble at that station
    interpolator = iris.analysis.Linear().interpolator(field, 
                                       ['latitude', 'longitude'])
    for y in range(0,len(kwargs.get('stations'))):
        station=kwargs.get('stations')[y]
        ensemble=interpolator([kwargs.get('station_latlon')[station]['latitude'],
                               kwargs.get('station_latlon')[station]['longitude']])

        ax.scatter(ensemble.data,
                    numpy.linspace(y+1.25,y+1.75,
                                  num=len(ensemble.data)),
                    kwargs.get('scatter_point_size'),
                    'blue', # Color
                    marker='.',
                    edgecolors='face',
                    linewidths=0.0,
                    alpha=kwargs.get('scatter_alpha'),
                    zorder=0.5)

