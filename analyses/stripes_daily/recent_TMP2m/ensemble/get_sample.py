# Get the sample cube for 20CR-daily
# Sample in the ensemble.
# Resolved in latitude, average in longitude.

import os
import iris
import numpy
import datetime
from iris.experimental.equalise_cubes import equalise_attributes
import sys
import pickle

def load_daily(year,month,day):
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
    return(e)

def get_sample_cube(year,month,day,climatology,
                    new_grid=None):

    h=load_daily(year,month,day)
    h -= climatology

    if new_grid is not None:
        h = h.regrid(new_grid,iris.analysis.Nearest())
                            
    # Average in Longitude
    s=h.data.shape
    ndata=numpy.ma.array(numpy.zeros((1,s[1])),mask=True)
    for lat in range(s[1]):
        m=numpy.random.randint(0,80)
        ndata[0,lat]=numpy.mean(h.data[m,lat,:])
            
    return ndata

