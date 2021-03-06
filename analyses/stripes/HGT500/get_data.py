#!/usr/bin/env python

# Download the 20CRv3 monthly-mean HGT500.

import os
import subprocess
import tarfile

base_url="https://portal.nersc.gov/archive/home/projects/incite11/www/20C_Reanalysis_version_3/everymember_anal_netcdf/mnmean/HGT500"

local_dir="%s/20CR/version_3/monthly_means" % os.getenv('SCRATCH')

for year in range(1806,2016):
    tf = "%s/%04d/HGT500.%04d.mnmean_mem039.nc" % (local_dir,year,year)
    if os.path.isfile(tf): continue
    remote = "%s/HGT500_%04d_mnmean.tar" % (base_url,year)
    local = "%s/HGT500_%04d_mnmean.tar" % (local_dir,year)
    if not os.path.exists(os.path.dirname(local)):
        os.makedirs(os.path.dirname(local))
    if not os.path.isfile(local):
        cmd="wget -O %s %s" % (local,remote)
        wg_retvalue=subprocess.call(cmd,shell=True)
        if wg_retvalue!=0:
            raise Exception("Failed to retrieve data")
    tf = tarfile.open(local)
    tf.extractall(path=local_dir)
    os.unlink(local)
    # Update the modification times on the files or SCRATCH
    #  will just delete them all again
    ncfs=os.listdir("%s/%04d" % (local_dir,year))
    for ncf in ncfs:
        os.utime("%s/%04d/%s" % (local_dir,year,ncf), None)
