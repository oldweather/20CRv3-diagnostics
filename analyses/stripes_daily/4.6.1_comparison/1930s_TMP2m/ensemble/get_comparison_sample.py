# Get the sample cube for EUSTACE-20CR daily
# Sample in the ensemble.
# Resolved in latitude, average in longitude.

import os
import iris
import IRData.twcr as twcr
import numpy
import datetime
from iris.experimental.equalise_cubes import equalise_attributes
import sys
import pickle

def load_daily_20CR(year,month,day):
    e=[]
    for member in range(1,81):
         f=iris.load_cube('%s/20CR/version_3/%04d/TMP2m.%04d_mem%03d.nc' % 
                                                           (os.getenv('SCRATCH'),year,year,member),
                             iris.Constraint(name='air_temperature') &
                             iris.Constraint(time=lambda cell: \
                                             cell.point.year == year and \
                                             cell.point.month == month and \
                                             cell.point.day == day))
         f=f.collapsed('height', iris.analysis.MEAN)
         f=f.collapsed('time', iris.analysis.MEAN)
         f.attributes=None
         f.add_aux_coord(iris.coords.AuxCoord(member, long_name='member'))         
         e.append(f)
    e=iris.cube.CubeList(e).merge_cube()
    coord_s=iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)
    e.coord('latitude').coord_system=coord_s
    e.coord('longitude').coord_system=coord_s
    return(e)

def load_daily_scout(year,month,day):
    e=[]
    for hour in (0,3,6,9,12,15,18,21):
         f=twcr.load('tmp',datetime.datetime(year,month,day,hour),height=2,version='4.6.1')
         e.append(f)
    e=iris.cube.CubeList(e).merge_cube()
    e=e.collapsed('time', iris.analysis.MEAN)
    return(e)

def get_sample_cube(year,month,day,
                    climatology_20CR,
                    climatology_scout,
                    new_grid=None):

    h2 = load_daily_20CR(year,month,day)
    h2 -= climatology_20CR
    if new_grid is not None:
        h2 = h2.regrid(new_grid,iris.analysis.Nearest())

    h = load_daily_scout(year,month,day)
    for idx in range(80):
        h.data[idx,:,:] -= climatology_scout.data
    if new_grid is not None:
        h = h.regrid(new_grid,iris.analysis.Nearest())

    # Average in Longitude
    s=h.data.shape
    ndata=numpy.ma.array(numpy.zeros((1,s[1])),mask=True)
    for lat in range(s[1]):
        m2=numpy.random.randint(0,80)
        me=numpy.random.randint(0,80)
        ndata[0,lat]=numpy.mean(h.data[me,lat,:]-h2.data[m2,lat,:])
            
    return ndata

