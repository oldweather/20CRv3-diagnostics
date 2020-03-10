# Get the sample cube for EUSTACE-20CR daily
# Sample in the ensemble.
# Resolved in latitude, average in longitude.

import os
import iris
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
    return(e)

def load_daily_EUSTACE(year,month,day):
    e=[]
    for member in range(10):
         f=iris.load_cube('%s/EUSTACE/1.0/%04d/tas_global_eustace_0_%04d%02d%02d.nc' %
                             (os.getenv('SCRATCH'),year,year,month,day),
                             iris.Constraint(cube_func=(lambda cell: \
                              cell.var_name == 'tasensemble_%d' % member)))
         f=f.collapsed('time', iris.analysis.MEAN)
         f.attributes=None
         f.var_name='tasensemble'
         f.add_aux_coord(iris.coords.AuxCoord(member, long_name='member'))      
         e.append(f)
    e=iris.cube.CubeList(e).merge_cube()
    return(e)

def get_sample_cube(year,month,day,
                    climatology_20CR,
                    climatology_EUSTACE,
                    new_grid=None):

    if new_grid is None:
        new_grid=climatology_EUSTACE

    h = load_daily_EUSTACE(year,month,day)
    for idx in range(10):
        h.data[idx,:,:] -= climatology_EUSTACE.data
    h = h.regrid(new_grid,iris.analysis.Nearest())

    h2 = load_daily_20CR(year,month,day)
    h2 -= climatology_20CR
    h2 = h2.regrid(new_grid,iris.analysis.Nearest())

    # Average in Longitude
    s=h.data.shape
    ndata=numpy.ma.array(numpy.zeros((1,s[1])),mask=True)
    for lat in range(s[1]):
        m2=numpy.random.randint(0,80)
        me=numpy.random.randint(0,10)
        ndata[0,lat]=numpy.mean(h.data[me,lat,:]-h2.data[m2,lat,:])
        rand_l = numpy.random.randint(0,s[2])
        if numpy.ma.count_masked(h.data[me,lat,:]) > rand_l:
               ndata.mask[0,lat]=True
            
    return ndata

