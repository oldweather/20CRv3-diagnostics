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

def get_sample_cube(year,month,day,climatology,
                    new_grid=None):

    h=load_daily(year,month,day)
    #h -= climatology # Doesn't work - why not?
    for idx in range(10):
        h.data[idx,:,:] -= climatology.data

    if new_grid is not None:
        h = h.regrid(new_grid,iris.analysis.Nearest())
                            
    # Average in Longitude
    s=h.data.shape
    ndata=numpy.ma.array(numpy.zeros((1,s[1])),mask=True)
    for lat in range(s[1]):
        m=numpy.random.randint(0,10)
        ndata[0,lat]=numpy.mean(h.data[m,lat,:])
        rand_l = numpy.random.randint(0,s[2])
        if numpy.ma.count_masked(h.data[m,lat,:]) > rand_l:
               ndata.mask[0,lat]=True
            
    return ndata

