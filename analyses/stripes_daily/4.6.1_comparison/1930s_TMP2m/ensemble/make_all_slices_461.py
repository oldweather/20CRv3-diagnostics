#!/usr/bin/env python

# Scripts to make slices for every day from scout 4.6.1

import os
import datetime

current=datetime.date(1930,10,1)
while current<datetime.date(1931,10,1):
    opf=("%s/20CR/version_4.6.1/analyses/Stripes_daily/TMP2m/"+
         "%04d%02d%02d.pkl") % (os.getenv('SCRATCH'),
                                current.year,current.month,current.day)
    if os.path.isfile(opf):
        current+=datetime.timedelta(days=1)
        continue
    print("./get_slice_461.py --year=%d --month=%d --day=%d" % (
                            current.year,current.month,current.day))
    current+=datetime.timedelta(days=1)
