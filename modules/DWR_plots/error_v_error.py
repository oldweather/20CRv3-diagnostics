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

# Plot reanalysis pressure and DWR comparisons - error v. error plots.

import numpy
import matplotlib

def plot_eve(ax,dmonth,**kwargs):
    """Plot obs-reanalysis against reanalysis sd

    Args:
        ax (:obj:`cartopy.axes`): Axes to hold the plot
        dmonth (:obj:`dict`): Components 'ensembles' and 'observations' each an array with the ensemble values and observation value at the time and place of each observation. 

    Kwargs:
        range (:obj:`list`): data range in scatterplot, default is (0,6).
        x_label (:obj:`str`): x label, default is 'Ensemble SD (hPa)'.
        y_label (:obj:`str`): y label, default is 'Ob-Ensemble mean RMS (hPa)'.
        point_size (:obj:`float`): Plot plot size, default 10.0.
        point_size (:obj:`str`): Plot plot color, default 'blue'.
        obs_errors (:obj:`list`): Assumed obs errors to show, default is (0,1,2)
        nbins (:obj:`int`): Resolution of plot - number of points.
    |
    """

    # Set keyword argument defaults
    kwargs.setdefault('range',(0.0,6.0))
    kwargs.setdefault('x_label','Ensemble SD (hPa)')
    kwargs.setdefault('y_label','Ob-Ensemble mean RMS (hPa)')
    kwargs.setdefault('point_size',100.0)
    kwargs.setdefault('point_color','blue')
    kwargs.setdefault('obs_errors',(0,1,2))
    kwargs.setdefault('nbins',50)

    # x & y-axis
    ax.set_xlim(kwargs.get('range'))
    ax.set_xlabel(kwargs.get('x_label'))
    ax.set_ylim(kwargs.get('range'))
    ax.set_ylabel(kwargs.get('y_label'))

    # Background line
    if kwargs.get('obs_errors') is not None:
        for o_error in kwargs.get('obs_errors'):
            x=numpy.linspace(kwargs.get('range')[0],
                             kwargs.get('range')[1])
            y=numpy.sqrt(numpy.square(x)+o_error**2)
            ax.add_line(matplotlib.lines.Line2D(
                        xdata=x,
                        ydata=y,
                        linestyle='solid',
                        linewidth=1,
                        color=(0.5,0.5,0.5,0.5),
                        zorder=1))

    # Calculate std of each ensemble
    ens_sd=[numpy.std(dmonth['ensembles'][idx][0],ddof=1) for idx in range(len(dmonth['ensembles']))]

    resolution=1/float(kwargs.get('nbins'))*100
    for idx in range(kwargs.get('nbins')):
        sd_min=numpy.percentile(ens_sd,idx*resolution)
        sd_max=numpy.percentile(ens_sd,(idx+1)*resolution)
        selected=[]
        x_select=[]
        for sdx in range(len(ens_sd)):
            if ens_sd[sdx]>=sd_min and ens_sd[sdx]<sd_max:
                selected.append(numpy.mean(dmonth['ensembles'][sdx][0])-
                                dmonth['observations'][sdx])
                x_select.append(ens_sd[sdx])

        if len(selected)<10: continue

        ax.scatter(numpy.mean(x_select),
                   numpy.sqrt(numpy.mean(numpy.square(selected))),
                   s=kwargs.get('point_size'),
                   marker='.',
                   alpha=1,
                   linewidths=0.01,
                   c=kwargs.get('point_color'))

def plot_vvv(ax,dmonth,**kwargs):
    """Plot obs-reanalysis against reanalysis variance

    Args:
        ax (:obj:`cartopy.axes`): Axes to hold the plot
        dmonth (:obj:`dict`): Components 'ensembles' and 'observations' each an array with the ensemble valuues and observation value at the time and place of each observation. 

    Kwargs:
        range (:obj:`list`): data range in scatterplot, default is (0,30).
        x_label (:obj:`str`): x label, default is 'Ensemble Variance (hPa**2)'.
        y_label (:obj:`str`): y label, default is 'Ob-Ensemble mean MS (hPa**2)'.
        point_size (:obj:`float`): Plot plot size, default 100.0.
        point_size (:obj:`str`): Plot plot color, default 'blue'.
        obs_errors (:obj:`list`): Assumed obs errors to show, default is (0,1,2)
        nbins (:obj:`int`): Resolution of plot - number of points.
    |
    """

    # Set keyword argument defaults
    kwargs.setdefault('range',(0.0,30.0))
    kwargs.setdefault('x_label','Ensemble Variance (hPa**2)')
    kwargs.setdefault('y_label','Ob-Ensemble mean MS (hPa**2)')
    kwargs.setdefault('point_size',100.0)
    kwargs.setdefault('point_color','blue')
    kwargs.setdefault('obs_errors',(0,1,2))
    kwargs.setdefault('nbins',50)

    # x & y-axis
    ax.set_xlim(kwargs.get('range'))
    ax.set_xlabel(kwargs.get('x_label'))
    ax.set_ylim(kwargs.get('range'))
    ax.set_ylabel(kwargs.get('y_label'))

    # Background line
    if kwargs.get('obs_errors') is not None:
        for o_error in kwargs.get('obs_errors'):
            x=numpy.linspace(kwargs.get('range')[0],
                             kwargs.get('range')[1])
            y=x+o_error**2
            ax.add_line(matplotlib.lines.Line2D(
                        xdata=x,
                        ydata=y,
                        linestyle='solid',
                        linewidth=1,
                        color=(0.5,0.5,0.5,0.5),
                        zorder=1))

    # Calculate variance of each ensemble
    ens_sd=[numpy.var(dmonth['ensembles'][idx][0],ddof=1) for idx in range(len(dmonth['ensembles']))]

    resolution=1/float(kwargs.get('nbins'))*100
    for idx in range(kwargs.get('nbins')):
        sd_min=numpy.percentile(ens_sd,idx*resolution)
        sd_max=numpy.percentile(ens_sd,(idx+1)*resolution)
        selected=[]
        x_select=[]
        for sdx in range(len(ens_sd)):
            if ens_sd[sdx]>=sd_min and ens_sd[sdx]<sd_max:
                selected.append(numpy.mean(dmonth['ensembles'][sdx][0])-
                                dmonth['observations'][sdx])
                x_select.append(ens_sd[sdx])

        if len(selected)<10: continue

        ax.scatter(numpy.mean(x_select),
                   numpy.mean(numpy.square(selected)),
                   s=kwargs.get('point_size'),
                   marker='.',
                   alpha=1,
                   linewidths=0.01,
                   c=kwargs.get('point_color'),
                   edgecolors=kwargs.get('point_color'))
