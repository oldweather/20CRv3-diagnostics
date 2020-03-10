#!/usr/bin/env python

# Scripts to make slices for every day

import os
import datetime

current=datetime.date(1926,1,1)
while current.year<1936:
    opf=("%s/EUSTACE/1.0/analyses/Stripes_daily/"+
         "%04d%02d%02d.pkl") % (os.getenv('SCRATCH'),
                                current.year,current.month,current.day)
    if os.path.isfile(opf):
        current+=datetime.timedelta(days=1)
        continue
    print("./get_slice.py --year=%d --month=%d --day=%d" % (
                            current.year,current.month,current.day),
          end=' ; ')
    if current.day%10==0:
        print("",end="\n")
    current+=datetime.timedelta(days=1)
