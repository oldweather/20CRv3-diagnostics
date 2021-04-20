#!/usr/bin/env python

# Retrieve archived 20CRv3 scout data from MASS

import sys
import os
import subprocess
import os.path
import glob
import re

# What to store
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--year", help="Year", type=int, required=True)
parser.add_argument("--month", help="Integer month", type=int, required=True)
parser.add_argument(
    "--version", help="Version, e.g. '4.5.1'", type=str, required=False, default="4.5.1"
)
parser.add_argument(
    "--variable",
    help="Variable name ('prmsl','observations,...)",
    type=str,
    required=False,
    default="all",
)
args = parser.parse_args()

# Base location for storage
mbase = "moose:/adhoc/projects/20cr/"
moose_dir = "%s/version_%s/%04d/%02d" % (mbase, args.version, args.year, args.month)

# Disc data dir
ddir = "%s/20CR/version_%s/" % (os.environ["SCRATCH"], args.version)
if not os.path.isdir(ddir):
    os.makedirs(ddir)

# Retrieve the observations
def retrieve_obs(year, month, version, variable):
    # Are they on disc
    ofiles = glob.glob("%s/observations/%04d/%04d%02d*.txt" % (ddir, year, year, month))
    if len(ofiles) > 100:
        return  # Already on disc

    proc = subprocess.Popen(
        "moo ls %s/observations_%04d%02d.tgz" % (moose_dir, year, month),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    (out, err) = proc.communicate()
    if len(err) != 0:
        if variable == "observations":
            raise Exception(
                "Obs file not on mass %s/observations_%04d%02d.tgz"
                % (moose_dir, year, month)
            )
        return

    # Retrieve ob file from MASS
    ody = "%s/observations/%04d" % (ddir, year)
    if not os.path.isdir(ody):
        os.makedirs(ody)
    proc = subprocess.Popen(
        "moo get %s/observations_%04d%02d.tgz %s/observations_%04d%02d.tgz"
        % (moose_dir, year, month, ody, year, month),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    (out, err) = proc.communicate()
    if len(err) != 0:
        print(err)
        raise Exception("Failed to retrieve observations from %s" % moose_dir)
    # Unack the month's obs
    otarf = "%s/observations/%04d/observations_%04d%02d.tgz" % (ddir, year, year, month)
    proc = subprocess.Popen(
        "cd %s ; tar xzf %s" % (ddir, otarf),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    (out, err) = proc.communicate()
    if len(err) != 0:
        print(err)
        raise Exception("Failed to untar observations")
    # Reset the modification time -
    #     otherwise scratch will delete them.
    members = glob.glob(
        "%s/observations/%04d/%04d%02d*/*.txt" % (ddir, year, year, month)
    )
    for member in members:
        os.utime(member, None)

    # Clean up
    os.remove(otarf)


# Retrieve a variable file
def retrieve_variable(year, month, version, variable):
    # Are they on disc
    ofiles = glob.glob("%s/%04d/%s.%04d%02d*.nc" % (ddir, year, variable, year, month))
    if len(ofiles) > 79:
        return  # Already on disc

    if not os.path.isdir("%s/%04d" % (ddir, year)):
        os.makedirs("%s/%04d" % (ddir, year))
    proc = subprocess.Popen(
        "moo get %s/%s_%04d%02d.tar %s" % (moose_dir, variable, year, month, ddir),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    (out, err) = proc.communicate()
    if len(err) != 0:
        print(err)
        raise Exception(
            "Failed to retrieve %s/%s_%04d%02d.tar" % (moose_dir, variable, year, month)
        )

    # Unack the month's data
    otarf = "%s/%s_%04d%02d.tar" % (ddir, variable, year, month)
    proc = subprocess.Popen(
        "cd %s ; tar xf %s" % (ddir, otarf),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    (out, err) = proc.communicate()
    if len(err) != 0:
        print(err)
        raise Exception("Failed to untar variable")
    # Reset the modification time -
    #     otherwise scratch will delete them.
    members = glob.glob(
        "%s/%04d/%s.%04d%02d_*.nc" % (ddir, year, variable, year, month)
    )
    for member in members:
        os.utime(member, None)

    # Clean up
    os.remove(otarf)


if args.variable == "all":
    proc = subprocess.Popen(
        "moo ls %s" % moose_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    (out, err) = proc.communicate()
    if len(err) != 0:
        print(err)
        raise Exception("Can't find any data in %s" % moose_dir)

    if len(re.findall(".*\.tgz", out.decode("utf-8"))) > 0:
        retrieve_obs(args.year, args.month, args.version, args.variable)

    for var in re.findall(".*\.tar", out.decode("utf-8")):
        variable = os.path.splitext(os.path.basename(var))[0]
        retrieve_variable(args.year, args.month, args.version, variable)
elif args.variable == "observations":
    retrieve_obs(args.year, args.month, args.version, args.variable)
else:
    retrieve_variable(args.year, args.month, args.version, args.variable)
