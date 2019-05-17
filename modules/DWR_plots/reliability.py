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

# Plot reanalysis pressure and DWR comparisons - scatter and error plots.

import iris
import iris.analysis
import DWR
import matplotlib
import matplotlib.cm
import numpy
import pandas
import collections

def plot_rotated_scatter(ax,field,obs,dte,**kwargs):
    """Make a scatter plot rotated so 1:1 is horizontal

    Args:
        ax (:`cartopy.axes`): Axes to hold the plot
        field (:obj:`iris.Cube.cube`): Reanalysis ensemble
        obs (:obj:`pandas.DataFrame`): DWR observations.
        dte (:obj:`datetime.datetime`): Time of plot

    Kwargs:
        x_range (:obj:`list`): x range in scatterplot, default is (945.0,1045.0).
        x_label (:obj:`str`): x label, default is 'Observed MSLP (hPa)'.
        y_range (:obj:`list`): y range in scatterplot, default is (-20.0,20.0).
        y_label (:obj:`str`): y label, default is 'Ensemble-Observed MSLP (hPa)'.
        point_size (:obj:`float`): Plot plot size, default 10.0.
        point_size (:obj:`str`): Plot plot color, default 'blue'.

    |
    """

    # Set keyword argument defaults
    kwargs.setdefault('x_range',(945.0,1045.0))
    kwargs.setdefault('x_label','Observed MSLP (hPa)')
    kwargs.setdefault('y_range',(-20.0,20.0))
    kwargs.setdefault('y_label','Ensemble-Observed MSLP (hPa)')
    kwargs.setdefault('point_size',10.0)
    kwargs.setdefault('point_color','blue')

    # x & y-axis
    ax.set_xlim(kwargs.get('x_range'))
    ax.set_xlabel(kwargs.get('x_label'))
    ax.set_ylim(kwargs.get('y_range'))
    ax.set_ylabel(kwargs.get('y_label'))

    stations=list(collections.OrderedDict.fromkeys(obs.loc[:,'name']).keys())
    # Get a pressure interpolated to the selected time for each station
    interpolated={}
    for station in stations:
        try:
            interpolated[station]=DWR.at_station_and_time(
                                           obs,station,dte)
        except Exception:
            interpolated[station]=None

    # Get the reanalysis ensemble at the station locations
    ensemble={}
    interpolator = iris.analysis.Linear().interpolator(field, 
                                    ['latitude', 'longitude'])
    for station in stations:
        latlon=DWR.get_station_location(obs,station)
        ensemble[station]=interpolator([latlon['latitude'],
                                        latlon['longitude']]).data

    # Background 1-to-1 line
    ax.add_line(matplotlib.lines.Line2D(
                xdata=kwargs.get('x_range'),
                ydata=(0,0),
                linestyle='solid',
                linewidth=1,
                color=(0.5,0.5,0.5,1),
                zorder=1))

    # Plot the ensembles
    for station in stations:
        if interpolated[station] is None: continue
        obs_ens=[interpolated[station]]*len(ensemble[station])
        ens_dif=[ensemble[station][i]-obs_ens[i] 
                             for i in range(len(obs_ens))]
        ax.scatter(obs_ens,
                   ens_dif,
                   s=kwargs.get('point_size'),
                   marker='o',
                   c=kwargs.get('point_color'),
                   linewidths=0.1,
                   edgecolors=kwargs.get('point_color'))


def plot_deviation_spread(ax,field,obs,dte,**kwargs):
    """Make a plot comparing ensemble spread with expectation

    Args:
        ax (:`cartopy.axes`): Axes to hold the plot
        field (:obj:`iris.Cube.cube`): Reanalysis ensemble
        obs (:obj:`pandas.DataFrame`): DWR observations.
        dte (:obj:`datetime.datetime`): Time of plot

    Kwargs:
        x_range (:obj:`list`): x range in plot, default is (-20,20.0).
        x_label (:obj:`str`): x label, default is 'Observation-ensemble mean (hPa)'.
        y_range (:obj:`list`): y range in scatterplot, default is (0.0,10.0).
        y_label (:obj:`str`): y label, default is 'Ensemble standard deviation (hPa)'.
        point_size (:obj:`float`): Plot plot size, default 10.0.
        point_size (:obj:`str`): Plot plot color, default 'blue'.
        obs_error (:obj:`float`): Assumed observation error (hPa), default 2.0.

    |
    """

    # Set keyword argument defaults
    kwargs.setdefault('x_range',(-20.0,20.0))
    kwargs.setdefault('x_label','Observation-ensemble mean (hPa)')
    kwargs.setdefault('y_range',(0.0,10.0))
    kwargs.setdefault('y_label','Ensemble standard deviation (hPa)')
    kwargs.setdefault('point_size',30.0)
    kwargs.setdefault('point_color','blue')
    kwargs.setdefault('obs_error',2.0)

    # x & y-axis
    ax.set_xlim(kwargs.get('x_range'))
    ax.set_xlabel(kwargs.get('x_label'))
    ax.set_ylim(kwargs.get('y_range'))
    ax.set_ylabel(kwargs.get('y_label'))

    stations=list(collections.OrderedDict.fromkeys(obs.loc[:,'name']).keys())
    # Get a pressure interpolated to the selected time for each station
    interpolated={}
    for station in stations:
        try:
            interpolated[station]=DWR.at_station_and_time(
                                           obs,station,dte)
        except Exception:
            interpolated[station]=None

    # Get the reanalysis ensemble at the station locations
    ensemble={}
    interpolator = iris.analysis.Linear().interpolator(field, 
                                    ['latitude', 'longitude'])
    for station in stations:
        latlon=DWR.get_station_location(obs,station)
        ensemble[station]=interpolator([latlon['latitude'],
                                        latlon['longitude']]).data

    # Expected ensemble sd
    exp_x=numpy.arange(kwargs.get('x_range')[0],
                       kwargs.get('x_range')[1],0.01)
    exp_y=numpy.sqrt(numpy.maximum(exp_x**2-kwargs.get('obs_error')**2,0))
    ax.add_line(matplotlib.lines.Line2D(
                xdata=exp_x, ydata=exp_y,
                linestyle='solid',
                linewidth=1,
                color=(0.5,0.5,0.5,1),
                zorder=1))

    # Plot the ensembles
    for station in stations:
        if interpolated[station] is None: continue
        ax.scatter(numpy.mean(ensemble[station])-interpolated[station],
                       numpy.std(ensemble[station]),
                       s=kwargs.get('point_size'),
                       marker='o',
                       c=kwargs.get('point_color'),
                       linewidths=0.1,
                       edgecolors='black')


