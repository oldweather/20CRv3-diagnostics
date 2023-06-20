import os
import sys
import subprocess
import datetime
import tarfile
import zipfile

from v3_load import _get_data_file_name
from v3_load import _get_data_dir


def _get_remote_file_name(variable, year):
    """Get all data for one variable, for one year, from 20CR archive at NERSC.

    Data wil be stored locally in directory $SCRATCH/20CR, to be retrieved by :func:`load`. If the local file that would be produced already exists, this function does nothing.

    Args:
        variable (:obj:`str`): Variable to fetch (e.g. 'prmsl').
        year (:obj:`int`): Year to get data for.

    Will retrieve the data for the year of the given date-time. If the selected time is very close to the end of the calendar year, loading data for that time will also need data from the next calendar year (for interpolation). In this case, also fetch the data for the next calendar year.

    Raises:
        StandardError: If variable is not a supported value.

    |
    """

    remote_dir = (
        "https://portal.nersc.gov/archive/home/projects/incite11/www/"
        + "20C_Reanalysis_version_3/everymember_anal_netcdf/subdaily"
    )

    if variable == "observations":
        remote_file = (
            "https://portal.nersc.gov/m958/v3_observations/" + "%04d.zip"
        ) % year
        return remote_file

    remote_file = "%s/%s/%s_%04d.tar" % (remote_dir, variable, variable, year)
    return remote_file


def _get_tar_file_name(variable, year):
    return "%s/%s_%04d.tar" % (_get_data_dir(), variable, year)


def _unpack_downloaded(variable, year):
    local_file = _get_tar_file_name(variable, year)
    tar = tarfile.open(local_file, "r")
    local_dir = os.path.dirname(local_file)
    tar.extractall(path=local_dir)
    tar.close()
    # Update the extracted file times
    #  To stop SCRATCH deleting them as too old
    nfiles = os.listdir("%s/%04d" % (local_dir, year))
    for nfile in nfiles:
        os.utime("%s/%04d/%s" % (local_dir, year, nfile))
    # os.remove(local_file)


def fetch(variable, dtime):
    ndtime = dtime + datetime.timedelta(hours=6)
    if ndtime.year != dtime.year:
        fetch(variable, ndtime)

    local_file = _get_data_file_name(variable, dtime.year)

    if os.path.isfile(local_file):
        # Got this data already
        return

    if not os.path.exists(os.path.dirname(local_file)):
        os.makedirs(os.path.dirname(local_file))

    remote_file = _get_remote_file_name(variable, dtime.year)

    # Download the tar file
    cmd = "wget -O %s %s" % (_get_tar_file_name(variable, dtime.year), remote_file)
    wg_retvalue = subprocess.call(cmd, shell=True)
    if wg_retvalue != 0:
        raise Exception("Failed to retrieve data")
    _unpack_downloaded(variable, dtime.year)


def _observations_zip_file(year, version="3"):
    return "%s/observations/%04d.zip" % (_get_data_dir(), year)


def _observations_file_name(year, month, day, hour, version="3"):
    # Two possible locations, and might be compressed
    of = "%s/observations/%04d/%04d%02d%02d%02d_psobs_posterior.txt" % (
        _get_data_dir(version),
        year,
        year,
        month,
        day,
        hour,
    )
    if os.path.isfile(of):
        return of
    of = "%s.gz" % of
    if os.path.isfile(of):
        return of
    of = "%s/observations/%04d/%04d%02d%02d%02d/psobs_posterior.txt" % (
        _get_data_dir(version),
        year,
        year,
        month,
        day,
        hour,
    )
    if os.path.isfile(of):
        return of
    of = "%s.gz" % of
    if os.path.isfile(of):
        return of
    return None


def _observations_remote_file(year):
    remote_file = (
        "https://portal.nersc.gov/project/m958/v3_observations/" + "%04d.zip"
    ) % year
    return remote_file


def fetch_observations(dtime):
    ndtime = dtime + datetime.timedelta(hours=6)
    if ndtime.year != dtime.year:
        fetch_observations(ndtime)
    o_dir = "%s/observations/%04d" % (_get_data_dir(), dtime.year)
    if os.path.exists(o_dir):
        if len(os.listdir(o_dir)) >= 1460:
            return
    _download_observations(dtime.year)
    _unpack_downloaded_observations(dtime.year)


def _download_observations(year):
    remote_file = _observations_remote_file(year)
    local_file = _observations_zip_file(year)
    if os.path.isfile(local_file):
        return
    if not os.path.exists(os.path.dirname(local_file)):
        os.makedirs(os.path.dirname(local_file))
    cmd = "wget -O %s %s" % (local_file, remote_file)
    wg_retvalue = subprocess.call(cmd, shell=True)
    if wg_retvalue != 0:
        os.remove(local_file)
        raise Exception("Failed to retrieve data")


def _unpack_downloaded_observations(year):
    local_file = _observations_zip_file(year)
    zf = zipfile.ZipFile(local_file)
    zf.extractall("%s/observations/" % _get_data_dir())
    os.remove(local_file)
