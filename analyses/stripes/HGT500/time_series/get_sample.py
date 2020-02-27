# Get the sample cube for 20CR
# Sample in the ensemble.
# Resolved in latitude, average in longitude.

import os
import iris
import numpy
import datetime
from iris.experimental.equalise_cubes import equalise_attributes
import sys
import pickle

def get_sample(min_lon=-180,max_lon=360,min_lat=-90,max_lat=90,
                    start=datetime.datetime(1851,1,1,0,0),
                    end=datetime.datetime(1900,12,31,23,59),
                    climatology=None,
                    climstart=1961,climend=1991,
                    new_grid=None):

    # Load the model data
    e=[]
    dts=None
    for member in range(1,81):
        m = []
        for year in range(start.year,end.year+1):
            
            h=iris.load_cube('%s/20CR/version_3/monthly_means/%04d/HGT500.%04d.mnmean_mem%03d.nc' % 
                                                               (os.getenv('SCRATCH'),year,year,member),
                             iris.Constraint(name='geopotential_height') &
                                                          iris.Constraint(time=lambda cell: \
                                             start <= cell.point <=end))
            h=h.collapsed('air_pressure', iris.analysis.MEAN)
            h.remove_coord('air_pressure')
            dty=h.coords('time')[0].units.num2date(h.coords('time')[0].points)

            # Anomalise
            if climatology is not None:
                for tidx in range(len(dty)):
                    midx=dty[tidx].month-1
                    h.data[tidx,:,:] -= climatology[midx].data

            if new_grid is not None:
                h = h.regrid(new_grid,iris.analysis.Nearest())
    
            # Reduce to area of interest
            h.coord('latitude').guess_bounds()
            h.coord('longitude').guess_bounds()
            h=h.extract(iris.Constraint(longitude=lambda v: min_lon <= v <= max_lon,
                                        latitude =lambda v: min_lat <= v <= max_lat))
                
            h.attributes=None
            h2=h
            if len(m)>0:
                # Workaround for metadata bug from varying versions of HDF library
                h2=m[0].copy()
                h2.data=h.data
                h2.remove_coord('time')
                h2.add_dim_coord(h.coord('time'),data_dim=0)
            m.append(h2)

        e.append(iris.cube.CubeList(m).concatenate_cube())

        if member==1:
            if dts is None:
                dts=dty
            else:
                dts=numpy.concatenate(dts,dty)
            
    # Get area averages
    ntp=e[0].data.shape[0]
    w = iris.analysis.cartography.area_weights(e[0])
    ndata=numpy.ma.array(numpy.zeros((ntp,80)),mask=True)
    for t in range(ntp):
        for m in range(80):
           ndata[:,m]=e[m].collapsed(['latitude', 'longitude'],
                                     iris.analysis.MEAN,
                                     weights=w).data
            
    return (ndata,dts)

