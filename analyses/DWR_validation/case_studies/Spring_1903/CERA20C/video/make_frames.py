#!/usr/bin/env python

# Make all the individual frames for a movie
#  run the jobs on SPICE.

import os
import sys
import subprocess
import datetime

max_jobs_in_queue=500
# Where to put the output files
opdir="%s/slurm_output" % os.getenv('SCRATCH')
if not os.path.isdir(opdir):
    os.makedirs(opdir)

start_day=datetime.datetime(1903, 1,  1, 13)
end_day  =datetime.datetime(1903, 3, 31, 11)

# Output directory
opd="%s/images/DWR/vcs_cera20c_1903_scatter+contour" % os.getenv('SCRATCH')

# Get file name from date
def opfile(dte):
   return "%s/Scatter+contour_%04d%02d%02d%02d%02d.png" % (
           opd,dte.year,dte.month,dte.day,dte.hour,dte.minute)

# Function to check if the job is already done for this timepoint
def is_done(dte):
    if os.path.isfile(opfile(dte)):
        return True
    return False

current_day=start_day
while current_day<=end_day:
    queued_jobs=subprocess.check_output('squeue --user hadpb',
                                         shell=True).count('\n')
    max_new_jobs=max_jobs_in_queue-queued_jobs
    while max_new_jobs>0 and current_day<=end_day:
        f=open("multirun.slm","w+")
        f.write('#!/bin/ksh -l\n')
        f.write(("#SBATCH --output=%s/sc_frame_"+
                 "%04d%02d%02d%02d.out\n") %
                   (opdir,
                    current_day.year,current_day.month,
                    current_day.day,current_day.hour))
        f.write('#SBATCH --qos=normal\n')
        f.write('#SBATCH --ntasks=4\n')
        f.write('#SBATCH --ntasks-per-core=1\n')
        f.write('#SBATCH --mem=40000\n')
        f.write('#SBATCH --time=5\n')
        count=0
        for minute in (0,15,30,45):
            if is_done(datetime.datetime(current_day.year,
                                         current_day.month,
                                         current_day.day,
                                         current_day.hour,
                                         minute)):
                continue
            cmd=("../../../../scripts/scatter+contour.py "+
                 " --year=%d --month=%d "+
                 "--day=%d --hour=%f "+
                 "--opdir=%s "+
                 "--reanalysis=cera "+
                 "--video "+
                 "--skip=BODO "+
                 "--skip=HAPARANDA "+
                 "--skip=HERNOSAND "+
                 "--skip=STOCKHOLM "+
                 "--skip=WISBY "+
                 "--skip=FANO "+
                 "--skip=BERLIN "+
                 "--skip=ABERDEEN "+
                 "--skip=VALENCIA "+
                 "--skip=JERSEY "+
                 "--skip=LISBON &\n") % (
                   current_day.year,current_day.month,
                   current_day.day,current_day.hour+minute/60.0,
                   opd)
            f.write(cmd)
            count=count+1
        f.write('wait\n')
        f.close()
        current_day=current_day+datetime.timedelta(hours=1)
        if count>0:
            max_new_jobs=max_new_jobs-1
            rc=subprocess.call('sbatch multirun.slm',shell=True)
        os.unlink('multirun.slm')
