import os
import os.path
import iris
import iris.time
import iris.coord_systems
import iris.fileformats
import datetime
import warnings
import numpy as np
import pandas


# Need to add coordinate system metadata so they work with cartopy
coord_s = iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)


def _get_data_dir(version="3"):
    """Return the root directory containing 20CR netCDF files"""
    g = "%s/20CR/version_%s/" % (os.environ["SCRATCH"], version)
    return g


def _get_data_file_name(variable, year, month=None, version="3", member=1):
    """Return the name of the file containing data for the
    requested variable, at the specified time, from the
    20CR version."""
    base_dir = _get_data_dir(version=version)
    # If monthly file exists, use that, otherwise, annual file
    if month is not None:
        name = "%s/%04d/%s.%04d%02d_mem%03d.nc" % (
            base_dir,
            year,
            variable,
            year,
            month,
            member,
        )
    if month is None or not os.path.isfile(name):
        name = "%s/%04d/%s.%04d_mem%03d.nc" % (
            base_dir,
            year,
            variable,
            year,
            member,
        )
    return name


def _is_in_file(variable, hour):
    """Is the variable available for this time?
    Or will it have to be interpolated?"""
    if hour % 3 == 0:
        return True
    return False


def _get_previous_field_time(variable, year, month, day, hour):
    """Get the latest time, before the given time,
    for which there is saved data"""
    return {"year": year, "month": month, "day": day, "hour": int(hour / 3) * 3}


def _get_next_field_time(variable, year, month, day, hour):
    """Get the earliest time, after the given time,
    for which there is saved data"""
    dr = {"year": year, "month": month, "day": day, "hour": int(hour / 3) * 3 + 3}
    if dr["hour"] >= 24:
        d_next = datetime.date(dr["year"], dr["month"], dr["day"]) + datetime.timedelta(
            days=1
        )
        dr = {
            "year": d_next.year,
            "month": d_next.month,
            "day": d_next.day,
            "hour": dr["hour"] - 24,
        }
    return dr


def _get_slice_at_hour_at_timestep(
    variable, year, month, day, hour, version="3", member=None
):
    """Get the cube with the data, given that the specified time
    matches a data timestep."""
    if not _is_in_file(variable, hour):
        raise ValueError("Invalid hour - data not in file")
    if member is None:
        res = iris.cube.CubeList()
        for mem in range(1, 81):
            res.append(
                _get_slice_at_hour_at_timestep(
                    variable, year, month, day, hour, version=version, member=mem
                )
            )
            if mem > 1:
                res[mem - 1].attributes = res[0].attributes
            res[mem - 1].add_aux_coord(iris.coords.AuxCoord(mem, long_name="member"))
        return res.merge_cube()
    file_name = _get_data_file_name(
        variable, year, month, version=version, member=member
    )
    time_constraint = iris.Constraint(
        time=iris.time.PartialDateTime(year=year, month=month, day=day, hour=hour)
    )
    try:
        with warnings.catch_warnings():  # Iris is v.fussy
            warnings.simplefilter("ignore")
            hslice = iris.load_cube(file_name, time_constraint)
    except iris.exceptions.ConstraintMismatchError:
        raise Exception(
            "%s not available for %04d-%02d-%02d:%02d"
            % (variable, year, month, day, hour)
        )

    # Enhance the names and metadata for iris/cartopy
    hslice.coord("latitude").coord_system = coord_s
    hslice.coord("longitude").coord_system = coord_s
    # Get rid of unnecessary height dimensions
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            hslice = hslice.collapsed("height", iris.analysis.MEAN)
    except Exception:
        pass
    return hslice


def load(variable, dtime, version="3", member=None):
    """Load requested data from disc, interpolating if necessary.

    Data must be available in directory $SCRATCH/20CR.

    Args:
        variable (:obj:`str`): Variable to fetch (e.g. 'prmsl')
        dtime (:obj:`datetime.datetime`): Date and time to load data for.
        version (:obj:`str`): Reanalysis version (e.g. '4.5.1') defaults to '3'
        member (:obj:`int`): Which member to load. Defaults to None - load all 80 members.

    Returns:
        :obj:`iris.cube.Cube`: Global field of variable at time.

    Note that 20CR data is only output every 3 hours, so if hour%3!=0, the result may be linearly interpolated in time.

    Raises:
        StandardError: Data not on disc.

    |
    """
    dhour = dtime.hour + dtime.minute / 60.0 + dtime.second / 3600.0
    if _is_in_file(variable, dhour):
        return _get_slice_at_hour_at_timestep(
            variable,
            dtime.year,
            dtime.month,
            dtime.day,
            dhour,
            version=version,
            member=member,
        )
    previous_step = _get_previous_field_time(
        variable, dtime.year, dtime.month, dtime.day, dhour
    )
    next_step = _get_next_field_time(
        variable, dtime.year, dtime.month, dtime.day, dhour
    )
    dt_current = dtime
    dt_previous = datetime.datetime(
        previous_step["year"],
        previous_step["month"],
        previous_step["day"],
        previous_step["hour"],
    )
    dt_next = datetime.datetime(
        next_step["year"], next_step["month"], next_step["day"], next_step["hour"]
    )
    s_previous = _get_slice_at_hour_at_timestep(
        variable,
        previous_step["year"],
        previous_step["month"],
        previous_step["day"],
        previous_step["hour"],
        version=version,
        member=member,
    )
    s_next = _get_slice_at_hour_at_timestep(
        variable,
        next_step["year"],
        next_step["month"],
        next_step["day"],
        next_step["hour"],
        version=version,
        member=member,
    )
    # Iris won't merge cubes with different attributes
    s_previous.attributes = s_next.attributes
    s_next = iris.cube.CubeList((s_previous, s_next)).merge_cube()
    s_next = s_next.interpolate([("time", dt_current)], iris.analysis.Linear())
    return s_next


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


def load_observations_1file(dtime, version):
    """Retrieve all the observations for an individual assimilation run."""
    of_name = _observations_file_name(
        dtime.year, dtime.month, dtime.day, dtime.hour, version=version
    )
    if not os.path.isfile(of_name):
        raise IOError("No obs file for given version and date")

    o = pandas.read_fwf(
        of_name,
        colspecs=[
            (0, 19),
            (20, 50),
            (52, 64),
            (66, 68),
            (69, 72),
            (74, 80),
            (81, 87),
            (88, 95),
            (97, 102),
            (103, 110),
            (111, 112),
            (113, 123),
            (124, 134),
            (135, 145),
            (146, 156),
            (157, 167),
            (168, 175),
            (176, 183),
            (184, 191),
            (192, 200),
            (201, 205),
            (206, 213),
            (214, 221),
            (222, 223),
        ],
        header=None,
        encoding="ISO-8859-1",
        names=[
            "UID",
            "Name",
            "ID",
            "Type",
            "NCEP.Type",
            "Longitude",
            "Latitude",
            "Observed",
            "Time.offset",
            "Observed.2",
            "Skipped",
            "Bias.correction",
            "Obfit.prior",
            "Obfit.post",
            "Obsprd.prior",
            "Obsprd.post",
            "Oberrvar.orig.out",
            "Oberrvar.out",
            "Oberrvar.use",
            "Paoverpb.save",
            "Prob.gross.error",
            "Localization.length.scale",
            "Lnsigl",
            "QC.failure.flag",
        ],
        converters={
            "UID": str,
            "Name": str,
            "ID": str,
            "Type": str,
            "NCEP.Type": int,
            "Longitude": float,
            "Latitude": float,
            "Observed": float,
            "Time.offset": float,
            "Observed.2": float,
            "Skipped": int,
            "Bias.correction": float,
            "Obfit.prior": float,
            "Obfit.post": float,
            "Obsprd.prior": float,
            "Obsprd.post": float,
            "Oberrvar.orig.out": float,
            "Oberrvar.out": float,
            "Oberrvar.use": float,
            "Paoverpb.save": float,
            "Prob.gross.error": float,
            "Localization.length.scale": float,
            "Lnsigl": float,
            "QC.failure.flag": int,
        },
        na_values=[
            "NA",
            "*",
            "***",
            "*****",
            "*******",
            "**********",
            "-99",
            "9999",
            "-999",
            "9999.99",
            "10000.0",
            "-9.99",
            "999999999999",
            "9",
        ],
        comment=None,
        compression="infer",
    )
    return o


def load_observations(start, end, version="3"):
    result = None
    ct = start
    while ct < end:
        if int(ct.hour) % 6 != 0:
            ct = ct + datetime.timedelta(hours=1)
            continue
        o = load_observations_1file(ct, version=version)
        dtm = pandas.to_datetime(o.UID.str.slice(0, 10), format="%Y%m%d%H")
        o2 = o[(dtm >= start) & (dtm < end)]
        if result is None:
            result = o2
        else:
            result = pandas.concat([result, o2])
        ct = ct + datetime.timedelta(hours=1)
    return result


def load_observations_fortime(v_time, version="3"):
    result = None
    if v_time.hour % 6 == 0:
        result = load_observations_1file(v_time, version=version)
        result["weight"] = np.repeat(1, len(result.index))
        return result
    if v_time.hour % 6 <= 3:
        prev_time = v_time - datetime.timedelta(hours=v_time.hour % 6)
        prev_weight = 1.0
        result = load_observations_1file(prev_time, version=version)
        result["weight"] = np.repeat(prev_weight, len(result.index))
        return result
    prev_time = v_time - datetime.timedelta(hours=v_time.hour % 6)
    prev_weight = (3 - v_time.hour % 3) / 3.0
    result = load_observations_1file(prev_time, version=version)
    result["weight"] = np.repeat(prev_weight, len(result.index))
    next_time = prev_time + datetime.timedelta(hours=6)
    next_weight = 1 - prev_weight
    result2 = load_observations_1file(next_time, version=version)
    result2["weight"] = np.repeat(next_weight, len(result2.index))
    result = pandas.concat([result, result2])
    return result
