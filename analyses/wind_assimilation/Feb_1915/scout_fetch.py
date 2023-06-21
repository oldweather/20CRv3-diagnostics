import os
import subprocess
import getpass
import datetime

from scout_load import _get_data_file_name
from scout_load import _get_data_dir
from scout_load import _observations_file_name


def _get_remote_file_name(
    variable,
    year,
    month,
    version="5.7.6",
    user="pbrohan",
):
    remote_dir = (
        "%s@perlmutter-p1.nersc.gov:/pscratch1/sd/p/%s/" + "20CRv3.final/version_%s"
    ) % (user, user, version)

    remote_file = "%s/%04d/%02d/%s.nc4" % (remote_dir, year, month, variable)
    return remote_file


def fetch(
    variable,
    dtime,
    version="5.7.6",
    user="pbrohan",
):
    local_file = _get_data_file_name(variable, dtime.year, dtime.month, version=version)

    if not os.path.exists(os.path.dirname(local_file)):
        os.makedirs(os.path.dirname(local_file))

    remote_file = _get_remote_file_name(
        variable, dtime.year, dtime.month, version, user
    )

    # Single file - use scp
    cmd = "scp %s %s" % (remote_file, local_file)
    scp_retvalue = subprocess.call(cmd, shell=True)
    if scp_retvalue != 0:
        raise Exception("Failed to retrieve data. Code: %d" % scp_retvalue)


def _observations_remote_file(year, month, version, user="pbrohan"):
    return (
        "%s@perlmutter-p1.nersc.gov:/pscratch/sd/p/%s/"
        + "20CRv3.final/version_%s/%04d/%02d/observations/"
    ) % (user, user, version, year, month)


def fetch_observations(dtime, version="5.7.6", user="pbrohan"):
    ndtime = dtime + datetime.timedelta(hours=6)
    if ndtime.year != dtime.year:
        fetch_observations(ndtime, version=version, user=user)
    o_dir = "%s/observations/%04d" % (_get_data_dir(version), dtime.year)
    if os.path.exists(o_dir):
        if len(os.listdir(o_dir)) >= 1460 * 3:
            return
    else:
        os.makedirs(o_dir)

    # Multiple files, use rsync
    r_dir = _observations_remote_file(dtime.year, dtime.month, version, user)
    cmd = "rsync -Lr %s/ %s" % (r_dir, o_dir)
    scp_retvalue = subprocess.call(cmd, shell=True)  # Why need shell=True?
    if scp_retvalue != 0:
        raise Exception("Failed to retrieve observations. Code: %d" % scp_retvalue)
