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

# Plot reanalysis pressure and DWR observations

import iris
import iris.analysis
import matplotlib
import matplotlib.cm
import cartopy.crs as ccrs
import numpy
import pandas
import Meteorographica as mg
import collections

def plot_contour(ax,extent,dte,field,obs_r,dwr_obs,**kwargs):
    """Make a mslp contour plot with DWR observations

    Args:
        ax (:`cartopy.axes`): Axes to hold the plot
        extent (:obj:`list`) Plot extent (lon.min,lon.max,lat.min,lat.max)
        dte (:obj:`datetime.datetime`): Time of plot
        field (:obj:`iris.Cube.cube`): Reanalysis mslp ensemble
        obs_r (:obj:`pandas.DataFrame`): Reanalysis observations.
        dwr_obs (:obj:`pandas.DataFrame`): DWR observations.

    Kwargs:
        projection (:obj:`cartopy.crs`): Map projection to use, default UKV.
        obs_radius (:obj:`float`): Reanalysis obs plot size, default 0.15.
        contour_levels (:obj:`list`): Values to plot contours at, default numpy.arange(870,1050,10).
        contour_width (:obj:`float`): Width of member contour lines, default 0.1.
        contour_mask (:obj:`float`): Plot mean contours where spread < this, default 3.
        n_contours (:obj:`int`): Max. number of member contour to plot, default None - all members.
        label_mean_contour (:obj:`bool`): Label the mean contour lines? Default=True.
        dwr_color (:obj:`str`): Either a color name, or the string 'anomaly' (default) to color by pressure anomaly.
        dwr_anomaly_range (:obj:`float`): Anomaly color scale factor, default 20.
        dwr_radius (:obj:`float`): DWR obs plot size, default 0.25.
        stations (:obj:`list`): Names (DWR format) of stations to be included, default is stations in dwr_obs.
        station_latlon (:obj:`dict`): Latitiudes and Longitudes of stations to be included, default is taken from dwr_obs.

    |
    """

    # Set keyword argument defaults
    kwargs.setdefault('projection',ccrs.RotatedPole(pole_longitude=177.5,
                                                    pole_latitude=35.5))
    kwargs.setdefault('obs_radius',0.15)
    kwargs.setdefault('contour_levels',numpy.arange(870,1050,10))
    kwargs.setdefault('contour_width',0.1)
    kwargs.setdefault('contour_mask',3.0)
    kwargs.setdefault('n_contours',None)
    kwargs.setdefault('label_mean_contour',True)
    if dwr_obs is not None:
        kwargs.setdefault('dwr_color','anomaly')
        kwargs.setdefault('dwr_anomaly_range',20.0)
        kwargs.setdefault('dwr_radius',0.25)
        kwargs.setdefault('stations',list(collections.OrderedDict.fromkeys(
                                          dwr_obs.loc[:,'name']).keys()))
        if 'station_latlon' not in kwargs:
            latlon={}
            for station in kwargs.get('stations'):
               latlon[station]=DWR.get_station_location(dwr_obs,station)
            kwargs['station_latlon']=latlon

    ax.set_axis_off()
    ax.set_extent(extent,crs=kwargs.get('projection'))
    ax.background_patch.set_facecolor(ax.get_figure().get_facecolor())
    mg.background.add_grid(ax)
    land_img=ax.background_img(name='GreyT', resolution='low')
        
    # Plot the DWR obs
    if dwr_obs is not None:
        if kwargs.get('dwr_color')=='anomaly':
            cmap = matplotlib.cm.get_cmap('coolwarm')
            interpolator = iris.analysis.Linear().interpolator(field, 
                                       ['latitude', 'longitude'])
            interpolated={}
            for station in kwargs.get('stations'):
                try:
                    interpolated[station]=DWR.at_station_and_time(
                                                      dwr_obs,station,dte)
                except Exception:
                    interpolated[station]=None
                ensemble=interpolator([kwargs.get('station_latlon')[station]['latitude'],
                                       kwargs.get('station_latlon')[station]['longitude']])
                if interpolated[station] is None:
                    spoof=pandas.DataFrame(data={
                          'latitude' : kwargs.get('station_latlon')[station]['latitude'],
                          'longitude': kwargs.get('station_latlon')[station]['longitude'],
                          'values'   : 0},index=[0])
                    mg.observations.plot(ax,spoof,
                         lat_label='latitude',lon_label='longitude',
                         radius=kwargs.get('dwr_radius'),
                         facecolor='grey',edgecolor='black')
                else:
                    stn_diff=interpolated[station]-numpy.mean(ensemble.data)
                    dfn=max(0.01,min(0.99,
                       stn_diff/kwargs.get('dwr_anomaly_range')+0.5))
                    stn_color=cmap(dfn)
                    mg.observations.plot(ax,dwr_obs[dwr_obs['name']==station],
                         lat_label='latitude',lon_label='longitude',
                         radius=kwargs.get('dwr_radius'),
                         facecolor=stn_color,edgecolor='black',
                         zorder=5)
        else:
            for station in kwargs.get('stations'):
                mg.observations.plot(ax,dwr_obs[dwr_obs['name']==station],
                     lat_label='latitude',lon_label='longitude',
                     radius=kwargs.get('dwr_radius'),
                     facecolor=kwargs.get('dwr_color'),edgecolor='black',
                     zorder=5)

    # Plot the 20CR obs
    if obs_r is not None:
        if 'Assimilation.indicator' in obs_r.index: # in V2 only
            obs_s=obs_r.loc[(obs_r['Assimilation.indicator']==1)]
            if not obs_s.empty:
                mg.observations.plot(ax,obs_s,radius=kwargs.get('obs_radius'),
                         zorder=10)
            obs_s=obs_r.loc[(obs_r['Assimilation.indicator']==0)]
            if not obs_s.empty:
                mg.observations.plot(ax,obs_s,radius=kwargs.get('obs_radius'),
                                     facecolor='grey',edgecolor='yellow',
                                     zorder=100)
        else:
            if not obs_r.empty:
                mg.observations.plot(ax,obs_r,radius=kwargs.get('obs_radius'),
                                     zorder=100)
        
    # Contour spaghetti plot of ensemble members
    if kwargs.get('n_contours') is not None:
        field_r=field.extract(iris.Constraint(member=
               field.coord('member').points[0:kwargs.get('n_contours')]))
    else: field_r=field
    mg.pressure.plot(ax,field_r,type='spaghetti',
                     resolution=0.25,
                     levels=kwargs.get('contour_levels'),
                     colors='blue',
                     label=False,
                     linewidths=kwargs.get('contour_width'),
                     zorder=15)
    # Add the ensemble mean - with labels
    field_m=field.collapsed('member', iris.analysis.MEAN)
    field_s=field.collapsed('member', iris.analysis.STD_DEV)
    field_m.data[numpy.where(field_s.data>kwargs.get('contour_mask'))]=numpy.nan
    mg.pressure.plot(ax,field_m,
                   resolution=0.25,
                   levels=kwargs.get('contour_levels'),
                   colors='black',
                   label=kwargs.get('label_mean_contour'),
                   linewidths=2,
                   zorder=20)
