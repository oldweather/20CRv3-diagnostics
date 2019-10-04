#!/usr/bin/env python

# Make all the individual frames for a movie

import os
import subprocess
import datetime

# Where to put the output files
opdir="%s/slurm_output" % os.getenv('SCRATCH')
if not os.path.isdir(opdir):
    os.makedirs(opdir)

# Function to check if the job is already done for this timepoint
def is_done(year,month,day):
    op_file_name=("%s/images/20CRv3_observations/" +
                  "%04d%02d%02d.png") % (
                            os.getenv('SCRATCH'),
                            year,month,day)
    if os.path.isfile(op_file_name):
        return True
    return False

f=open("run.txt","w+")

start_day=datetime.datetime(1851,  1,  1,  0)
end_day  =datetime.datetime(2015, 12, 31, 23)

current_day=start_day
while current_day<=end_day:
    if is_done(current_day.year,current_day.month,
                   current_day.day):
        current_day=current_day+datetime.timedelta(days=10)
        continue
    cmd=("./plot_obs_coverage.py --year=%d --month=%d " +
         "--day=%d "+
         "\n") % (
           current_day.year,current_day.month,
             current_day.day)
    f.write(cmd)
    current_day=current_day+datetime.timedelta(days=10)
f.close()

