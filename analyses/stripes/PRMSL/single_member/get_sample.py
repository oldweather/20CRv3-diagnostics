# Get the sample cube for 20CR
# Single ensemble member.
# Resolved in latitude, average in longitude.

import os
import iris
import numpy
import datetime
from iris.experimental.equalise_cubes import equalise_attributes
import sys
import pickle

def get_sample_cube(start=datetime.datetime(1851,1,1,0,0),
                    end=datetime.datetime(1900,12,31,23,59),
                    climatology=None,
                    climstart=1961,climend=1991,
                    new_grid=None,rstate=None):

    # Might want the longitude random sampling to be reproducible
    if rstate is None:
        r_lon = numpy.random.RandomState(seed=None)
    else:
        r_lon = rstate

    # Make the climatology, if not supplied
    if climatology is None:
        climatology=[]
        e=[]
        for year in range(1961,1991):
             h = None
             for member in range(1,2):
                 f=iris.load_cube('%s/20CR/version_3/monthly_means/%04d/PRMSL.%04d.mnmean_mem%03d.nc' % 
                                                                   (os.getenv('SCRATCH'),year,year,member),
                                 iris.Constraint(name='Pressure reduced to MSL'))
                 if h is None:
                     h=f
                 else:
                     h.data += f.data
                     
             h.data /= 1
             h.attributes=None
             e.append(h)

        e=iris.cube.CubeList(e).concatenate_cube()

        for month in range(1,13):
             m=e.extract(iris.Constraint(time=lambda cell: cell.point.month == month))
             climatology.append(m.collapsed('time', iris.analysis.MEAN))

    # Load the model data
    e=[]
    dts=None
    for member in range(1,2):
        m = []
        for year in range(start.year,end.year+1):
            
            h=iris.load_cube('%s/20CR/version_3/monthly_means/%04d/PRMSL.%04d.mnmean_mem%03d.nc' % 
                                                               (os.getenv('SCRATCH'),year,year,member),
                             iris.Constraint(name='Pressure reduced to MSL') &
                             iris.Constraint(time=lambda cell: \
                                             start <= cell.point <=end))
            dty=h.coords('time')[0].units.num2date(h.coords('time')[0].points)

            # Anomalise
            for tidx in range(len(dty)):
                midx=dty[tidx].month-1
                h.data[tidx,:,:] -= climatology[midx].data

            if new_grid is not None:
                h = h.regrid(new_grid,iris.analysis.Nearest())
                
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

        if dts is None:
            dts=dty
        else:
            dts=numpy.concatenate(dts,dty)
            
    # Average in Longitude
    s=e[0].data.shape
    ndata=numpy.ma.array(numpy.zeros((s[0],s[1])),mask=True)
    for t in range(s[0]):
        for lat in range(s[1]):
            ndata[t,lat]=numpy.mean(e[0].data[t,lat,:])
            
    return (ndata,dts)

