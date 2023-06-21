#!/usr/bin/env python

# Make all the individual frames for a movie

import os
import datetime

# Where to put the output files
opdir="%s/slurm_output" % os.getenv('SCRATCH')
if not os.path.isdir(opdir):
    os.makedirs(opdir)

# Function to check if the job is already done for this timepoint
def is_done(year,month,day,hour):
    op_file_name=("%s/images/V3v576/" +
                  "V3v576_%04d%02d%02d%02d%02d.png") % (
                            os.getenv('SCRATCH'),
                            year,month,day,int(hour),
                                        int(hour%1*60))
    if os.path.isfile(op_file_name):
        return True
    return False


f=open("run.txt","w+")

start_day=datetime.datetime(1915, 2, 1, 6)
end_day  =datetime.datetime(1915, 2, 28, 18)

current_day=start_day
while current_day<=end_day:
    for fraction in (0,.25,.5,.75):
        if is_done(current_day.year,current_day.month,
                       current_day.day,current_day.hour+fraction):
            continue
        cmd=("./V3v576.py --year=%d --month=%d" +
            " --day=%d --hour=%f \n") % (
               current_day.year,current_day.month,
               current_day.day,current_day.hour+fraction)
        f.write(cmd)
    current_day=current_day+datetime.timedelta(hours=1)
f.close()
