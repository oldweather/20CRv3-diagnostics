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
def is_done(year,month,day,hour):
    op_file_name=("%s/images/xmas_1811/" +
                  "V3only_x11_%04d%02d%02d%02d%02d.png") % (
                            os.getenv('SCRATCH'),
                            year,month,day,int(hour),
                                        int(hour%1*60))
    if os.path.isfile(op_file_name):
        return True
    return False

f=open("run.txt","w+")

start_day=datetime.datetime(1811, 12, 18, 0)
end_day  =datetime.datetime(1811, 12, 26, 23)

current_day=start_day
while current_day<=end_day:
    for fraction in (0,.25,.5,.75):
        if is_done(current_day.year,current_day.month,
                       current_day.day,current_day.hour+fraction):
            continue
        cmd=("./x11_V3only.py --year=%d --month=%d" +
            " --day=%d --hour=%f \n") % (
               current_day.year,current_day.month,
               current_day.day,current_day.hour+fraction)
        f.write(cmd)
    current_day=current_day+datetime.timedelta(hours=1)
f.close()
