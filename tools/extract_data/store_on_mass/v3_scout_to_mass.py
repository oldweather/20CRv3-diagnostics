#!/usr/bin/env python

# Archive downloaded 20CRv3 scout data to MASS

import sys
import os
import subprocess
import os.path
import glob
import tarfile
sys.path.append('/data/users/afterburner/software/turbofan/v1.3.1/lib/python/')
import afterburner.io.moose2 as moose

# What to store
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--year", help="Year",
                    type=int,required=True)
parser.add_argument("--month", help="Integer month",
                    type=int,required=True)
parser.add_argument("--version", help="Version, e.g. '4.5.1'",
                    type=str,required=False,
                    default='4.5.1')
parser.add_argument("--variable", 
                    help="Variable name ('prmsl','observations,...)",
                    type=str,required=True)
args = parser.parse_args()

# Check moose availability
if not moose.has_moose_support():
    raise Exception("Moose unavailable")
if not moose.check_moose_commands_enabled(moose.MOOSE_LS):
    raise Exception("'moo ls' disabled")
if not moose.check_moose_commands_enabled(moose.MOOSE_PUT):
    raise Exception("'moo put' disabled")

# Base location for storage
mbase="moose:/adhoc/projects/20cr/"
moose_dir=("%s/version_%s/%04d/%02d" %
                (mbase,args.version,args.year,args.month))
if moose.run_moose_command('moo test %s' % moose_dir)[0]!='true':
# Make the moose directory
    moose.run_moose_command("moo mkdir -p %s" % moose_dir)

# Disc data dir
ddir="%s/20CR/version_%s" % (os.environ['SCRATCH'],args.version)

# Archive a field
def archive_fields(var,year,month,version):
    if moose.run_moose_command("moo test -f %s/%s_%04d%02d.tar" % 
                               (moose_dir,var,year,month))[0]=='true':
        return()  # Already archived
    # Are there any fields to archive?
    ofiles=glob.glob("%s/%04d/%s.%04d%02d_mem*.nc" %
                           (ddir,year,var,year,month))
    if len(ofiles)==0:  # No fields on disc
        raise Exception("No %s fields on disc for %04d-%02d %s" %
                                            (var,year,month,version))
        return()

    # Pack the month's fields into a single file
    otarf=("%s/%04d/%s_%04d%02d.tar" % 
                           (ddir,year,var,year,month))
    tf = tarfile.open(name=otarf,mode='w')
    blen = len(ddir)
    for of in ofiles:
        tf.add(of,arcname=of[blen:])
    tf.close()

    # Stow the ob file on MASS
    moose.put("%s/%04d" % (ddir,year),
              ['%s_%04d%02d.tar' % (var,year,month)],
              moose_dir)

    # Clean up
    os.remove(otarf)


# Archive the observations
def archive_obs(year,month,version):
    if moose.run_moose_command("moo test -f %s/observations_%04d%02d.tgz" % 
                               (moose_dir,year,month))[0]=='true':
        return()  # Already archived

    # Are there any observations to archive?
    ofiles=glob.glob("%s/observations/%04d/%04d%02d*.txt" %
                           (ddir,year,year,month))
    ofiles.extend(glob.glob("%s/observations/%04d/%04d%02d*.txt.gz" %
                           (ddir,year,year,month)))
    ofiles.extend(glob.glob("%s/observations/%04d/%04d%02d*/*.txt" %
                           (ddir,year,year,month)))
    ofiles.extend(glob.glob("%s/observations/%04d/%04d%02d*/*.txt.gz" %
                           (ddir,year,year,month)))
    if len(ofiles)==0:  # No obs on disc
        raise Exception("No obs on disc for %04d-%02d %s" %
                                            (year,month,version))
        return()

    # Pack the month's obs into a single file
    otarf=("%s/observations/%04d/observations_%04d%02d.tgz" % 
                           (ddir,year,year,month))
    tf = tarfile.open(name=otarf,mode='w:gz')
    blen = len(ddir)
    for of in ofiles:
        tf.add(of,arcname=of[blen:])
    tf.close()

    # Stow the ob file on MASS
    moose.put("%s/observations/%04d" % (ddir,year),
              ['observations_%04d%02d.tgz' % (year,month)],
              moose_dir)

    # Clean up
    os.remove(otarf)

if args.variable=='observations':
    archive_obs(args.year,args.month,args.version)
else:
    archive_fields(args.variable,args.year,args.month,args.version)
