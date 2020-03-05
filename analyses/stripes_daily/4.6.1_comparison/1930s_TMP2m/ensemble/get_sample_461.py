# Get the sample cube for 20CR-daily from scout 4.6.1
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

def load_daily(year,month,day):
    e=[]
    for hour in (0,3,6,9,12,15,18,21):
         f=twcr.load('tmp',datetime.datetime(year,month,day,hour),height=2,version='4.6.1')
         e.append(f)
    e=iris.cube.CubeList(e).merge_cube()
    e=e.collapsed('time', iris.analysis.MEAN)
    return(e)

def get_sample_cube(year,month,day,climatology,
                    new_grid=None):

    h=load_daily(year,month,day)
    for m in range(80):
        h.data[m,:,:]-=climatology.data

    if new_grid is not None:
        h = h.regrid(new_grid,iris.analysis.Nearest())
                            
    # Average in Longitude
    s=h.data.shape
    ndata=numpy.ma.array(numpy.zeros((1,s[1])),mask=True)
    for lat in range(s[1]):
        m=numpy.random.randint(0,80)
        ndata[0,lat]=numpy.mean(h.data[m,lat,:])
            
    return ndata

