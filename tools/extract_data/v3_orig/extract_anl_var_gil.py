#!/usr/bin/env python

# Extract 20CRv3 analysis variable from the full output

import os
import sys
import subprocess
import tempfile
import datetime

# Version and month
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--startyear", help="Year run started",
                    type=int, required=True)
parser.add_argument("--year", help="Year to extract",
                    type=int, required=True)
parser.add_argument("--month", help="Month to extract",
                    type=int, required=True)
parser.add_argument("--version", help="Month to extract",
                    type=int,default=451)
parser.add_argument("--var", help="Variable to extract",
                    type=str, required=True)
parser.add_argument("--level",help="Pressure level (hPa) to extract at",
                    type=str,default='None',required=False,
                    choices=['1000','975','950','925','900','850',
                             '800','750','700','650','600','550',
                             '500','450','400','350','300','250',
                             '200','150','100','70','50','30','20',
                             '10','5','1'])
parser.add_argument("--height",help="Height (m) to extract at",
                    type=str,default='None',required=False,
                    choices=['2','10','12','20','30','50','80',
                             '100','150','200','250','300','500'])
                             
args = parser.parse_args()

# Set default heights, where appropriate
if args.var=='air.2m':
    args.level=None
    args.height='2'
    args.var='TMP'
if args.var=='uwnd.10m':
    args.level=None
    args.height='10'
    args.var='UGRD'
if args.var=='vwnd.10m':
    args.level=None
    args.height='10'
    args.var='VGRD'

# Make an output file name
def opfile(var,level,height):
   var=var.lower()
   if var=='prmsl': return 'prmsl'
   if var=='air.sfc': return 'air.sfc'
   if var=='air.2m': return 'air.2m'
   if var=='tmp' and height is not None and height==2:
      return 'air.2m'
   if var=='uwnd' or var=='ugrd':
      if level is not None:
          return 'uwnd.%dmb' % int(level)
      if height is not None:
          return 'uwnd.%dm' % int(height)
      else:
          raise ValueError('Either height or level must be specified')
   if var=='vwnd' or var=='vgrd':
      if level is not None:
          return 'vwnd.%dmb' % int(level)
      if height is not None:
          return 'vwnd.%dm' % int(height)
      else:
          raise ValueError('Either height or level must be specified')
   if var=='icec':
      return 'icec'

   # Default - specify grib2 var directly
   if level is not None:
      return '%s.%dmb' % (var.lower(),int(level))
   if height is not None:
      return '%s.%dm' % (var.lower(),int(height))
   else:
      raise ValueError('Either height or level must be specified')


# Make a search string
def search_string(var,level,height):
   if var=='prmsl': return 'PRMSL'
   if var=='air.sfc': return 'TMP:surface'
   if var=='uwnd' or var=='ugrd':
      if level is not None:
          return 'UGRD:.*%d mb' % int(level)
      if height is not None:
          return 'UGRD:.*%d m above ground' % int(height)
      else:
          raise ValueError('Either height or level must be specified')
   if var=='vwnd' or var=='vgrd':
      if level is not None:
          return 'VGRD:.*%d mb' % int(level)
      if height is not None:
          return 'VGRD:.*%d m above ground' % int(height)
      else:
          raise ValueError('Either height or level must be specified')
   if var=='icec':
      return 'ICEC'

   # Default - specify grib2 var directly
   if level is not None:
      return '%s:.*%d mb' % (var.upper(),int(level))
   if height is not None:
      return '%s:.*%d m above ground' % (var.upper(),int(height))
   else:
      raise ValueError('Either height or level must be specified')
   
# Where to find the grib (and obs) files retrieved from hsi
working_directory="/global/cscratch1/sd/compo/gfsenkf_20crV3_cmip5oz_CoriII//ensda_461_%04d/" % args.startyear
#if not os.path.isdir(working_directory):
#    os.makedirs(working_directory)
# Where to put the final output files for this month
final_directory="%s/20CRv3.final/version_%1d.%1d.%1d/%04d/%02d" % (
                  os.getenv('SCRATCH'),int(args.version/100),
                  int((args.version%100)/10),int(args.version%10),
                  args.year,args.month)
if not os.path.isdir(final_directory):
    os.makedirs(final_directory)

# Use the wgrib utility for data extraction
wgrib='/global/homes/c/compo/bin/wgrib'

# Don't repeat pre-existing extractions
fn= "%s/%s.nc4" % (final_directory,opfile(args.var,args.level,args.height))
if os.path.isfile(fn):
    raise StandardError('Already done')

# Temporary file for staging extracted data
tfile=tempfile.NamedTemporaryFile(delete=False)

current_day=datetime.datetime(args.year,args.month,1,0)
while current_day.month==args.month:
    # Extract grids every 3 hours and concatenate to output
    for hour in range(0,24,3):
        if hour%6==0:
            subdir="%04d%02d%02d%02d" % (current_day.year,
              current_day.month,current_day.day,hour)
        for member in range(1,81):
            an_file_name= "%s/%s/pgrbanl_%04d%02d%02d%02d_mem%03d" % (
                            working_directory,subdir,
                            current_day.year,
                            current_day.month,current_day.day,
                            hour,member)
            if not os.path.exists(an_file_name):
                raise StandardError("Missing data %s" % an_file_name)

            proc = subprocess.Popen(
              "%s %s | grep '%s' | %s -i -grib %s -o %s; cat %s >> %s/%s.grb" % (
                         wgrib,an_file_name,
                         search_string(args.var,args.level,args.height),
                         wgrib,an_file_name,
                         tfile.name,tfile.name,
                         final_directory,
                         opfile(args.var,args.level,args.height)),shell=True)
            (out, err) = proc.communicate()
            if out is not None or err is not None:
                raise StandardError("Failed to extract %s from %s" % (
                                     opfile(args.var,args.level,args.height),
                                     an_file_name))
   
    current_day=current_day+datetime.timedelta(days=1)
os.remove(tfile.name)

# Convert to netCDF
proc = subprocess.Popen(
  "ncl_convert2nc %s.grb -i %s -o %s -L -nc4c -cl 5" % ( 
                        opfile(args.var,args.level,args.height),
                        final_directory,
                        final_directory),
                        shell=True)
(out, err) = proc.communicate()
if out is not None or err is not None:
    raise StandardError("Failed to convert %s to netCDF" % 
                         opfile(args.var,args.level,args.height))
# Strip out unnecessary dimensions that confuse iris
proc = subprocess.Popen("ncks -C -O -x -v ensemble0_info,initial_time1,initial_time1_encoded "+
                        "%s/%s.nc4 %s/%s.stripped.nc4" % (final_directory,
                                                          opfile(args.var,args.level,args.height),
                                                          final_directory,
                                                          opfile(args.var,args.level,args.height)),
                        shell=True)
(out, err) = proc.communicate()
if out is not None or err is not None:
    raise StandardError("Failed to strip %s netCDF file" % args.var)
os.rename("%s/%s.stripped.nc4" % (final_directory,opfile(args.var,args.level,args.height)),
          "%s/%s.nc4" % (final_directory,opfile(args.var,args.level,args.height)))
