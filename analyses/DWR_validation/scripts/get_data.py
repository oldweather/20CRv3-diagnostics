#!/usr/bin/env python

# Get data from the selected reanalysis, for the requested period

import IRData.twcr as twcr
import IRData.cera20c as cera20c
import datetime
import sys

# Get the datetime to plot from commandline arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--start", help="Start: yyyymm(dd(hh))",
                    type=str,required=True)
parser.add_argument("--end", help="End: yyyymm(dd(hh))",
                    type=str,required=True)
parser.add_argument("--reanalysis", help="20cr2c | 20cr3 | cera",
                    type=str,required=True)

args = parser.parse_args()

start=datetime.datetime(int(args.start[0:4]),
                        int(args.start[4:6]),
                        1,0)
if len(args.start) >= 8:
    start=start+datetime.timedelta(days=int(args.start[6:8]))
if len(args.start) >= 10:
    start=start+datetime.timedelta(hours=int(args.start[8:10]))

end=datetime.datetime(int(args.end[0:4]),
                      int(args.end[4:6]),
                      1,0)
if len(args.end) >= 8:
    end=end+datetime.timedelta(days=int(args.end[6:8]))
if len(args.end) >= 10:
    end=end+datetime.timedelta(hours=int(args.end[8:10]))

current=start
while current<end:

    if args.reanalysis=='20cr3':
        twcr.fetch('prmsl',current,version='4.5.1')
        twcr.fetch_observations(current,version='4.5.1')
    elif args.reanalysis=='20cr2c':
        twcr.fetch('prmsl',current,version='2c')
        twcr.fetch_observations(current,version='2c')
    elif args.reanalysis=='cera':
        cera20c.fetch('prmsl',current)
    else:
        print "Unsupported reanalysis %s" % args.reanalysis
        sys.exit(1)

    current=current+datetime.timedelta(days=28)
