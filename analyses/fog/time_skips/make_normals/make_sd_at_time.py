#!/usr/bin/env python

# Make standard deviations from 20CRv3 data 
#  for a given day and hour.

import os
import numpy
import iris
import IRData.twcr as twcr

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--var", help="Variable",
                    type=str,required=True)
parser.add_argument("--month", help="Integer month",
                    type=int,required=True)
parser.add_argument("--day", help="Day of month",
                    type=int,required=True)
parser.add_argument("--hour", help="Hour of day",
                    type=int,required=True)
parser.add_argument("--startyear", help="First year of climatology",
                    type=int,required=False,default=1981)
parser.add_argument("--endyear", help="First year of climatology",
                    type=int,required=False,default=2010)
args = parser.parse_args()

op_dir = "%s/20CR/version_3/sds/%s/climatology_%04d_%04d" % (
          os.getenv('DATADIR'),args.var,args.startyear,args.endyear)
if not os.path.isdir(op_dir):
    os.makedirs(op_dir)

if args.var=='PRMSL': 
    fname='prmsl'
    vname='air_pressure_at_sea_level'
if args.var=='TMP2m': 
    fname='air.2m'
    vname='air_temperature'

# Load the normal
normal=iris.load_cube(("%s/20CR/version_3/normals/%s/"+
                       "climatology_%04d_%04d/%02d%02d%02d.nc") % (
                        os.getenv('DATADIR'),args.var,
                        args.startyear,args.endyear,
                        args.month,args.day,args.hour))

accum = None  
for cyr in range (args.startyear,args.endyear+1):
    time_constraint=iris.Constraint(time=iris.time.PartialDateTime(
                                    year=cyr,
                                    month=args.month,
                                    day=args.day,
                                    hour=args.hour))
    name_constraint=iris.Constraint(name=vname)
    inst = iris.load_cube("%s/20CR/version_3/ensemble_means/%s/%s.%04d.nc" %
                          (os.getenv('SCRATCH'),args.var,fname,cyr),
                          time_constraint & name_constraint)
    if accum is None:
        accum = inst
        accum.data=(inst.data-normal.data)**2
    else:
        accum.data = accum.data + (inst.data-normal.data)**2

accum.data /= args.endyear-args.startyear+1
accum.data = numpy.sqrt(accum.data)

iris.save(accum,"%s/%02d%02d%02d.nc" % 
               (op_dir,args.month,args.day,args.hour))
