#!/usr/bin/env python

# Make climatology for V3 monthly data

import os
import iris
import numpy
import datetime
from iris.experimental.equalise_cubes import equalise_attributes
import sys
import pickle

cpkl="%s/20CR/version_3/monthly_means/HGT500.climatology.1961-90.pkl" % os.getenv('SCRATCH')

climatology=[]
e=[]
for year in range(1961,1991):
     h = None
     for member in range(1,81):
         f=iris.load_cube('%s/20CR/version_3/monthly_means/%04d/HGT500.%04d.mnmean_mem%03d.nc' % 
                                                           (os.getenv('SCRATCH'),year,year,member),
                         iris.Constraint(name='geopotential_height'))
         f=f.collapsed('air_pressure', iris.analysis.MEAN)
         if h is None:
             h=f
         else:
             h.data += f.data

     h.data /= 80
     h.attributes=None
     e.append(h)

e=iris.cube.CubeList(e).concatenate_cube()

for month in range(1,13):
     m=e.extract(iris.Constraint(time=lambda cell: cell.point.month == month))
     climatology.append(m.collapsed('time', iris.analysis.MEAN))

pickle.dump(climatology,open(cpkl,'wb'))
