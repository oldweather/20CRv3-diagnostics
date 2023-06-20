import os
import os.path
import iris
import iris.time
import iris.coord_systems
import iris.fileformats
import datetime
import warnings


# Need to add coordinate system metadata so they work with cartopy
coord_s = iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)

# Supported analysis variables
monolevel_analysis = (
    "prmsl",
    "air.2m",
    "uwnd.10m",
    "vwnd.10m",
    "icec",
    "sst",
    "air.sfc",
)
multilevel_analysis = ("tmp", "uwnd", "vwnd", "hgt", "spfh", "pvort")
# Suported forecast variables
monolevel_forecast = "prate"


def _get_data_dir(version="5.7.6"):
    """Return the root directory containing 20CR netCDF files"""
    g = "%s/20CR/version_%s/" % (os.environ["SCRATCH"], version)
    return g


def _get_data_file_name(
    variable, year, month, height=None, level=None, ilevel=None, version="5.7.6"
):
    """Return the name of the file containing data for the
    requested variable, at the specified time, from the
    20CR version."""
    base_dir = _get_data_dir(version)
    if variable in monolevel_analysis or variable in monolevel_forecast:
        name = "%s/%04d/%02d/%s.nc4" % (base_dir, year, month, variable)
    elif variable in multilevel_analysis:
        if level is not None:
            name = "%s/%04d/%02d/%s.%dmb.nc" % (base_dir, year, month, variable, level)
        elif ilevel is not None:
            name = "%s/%04d/%02d/%s.%dK.nc" % (base_dir, year, month, variable, ilevel)
        elif height is not None:
            name = "%s/%04d/%02d/%s.%dm.nc" % (base_dir, year, month, variable, height)
        else:
            raise ValueError("No height, level, or ilevel specified for 3d variable")
    else:
        raise ValueError("Unsupported variable: %s" % variable)
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


def _time_to_time(variable, year, month, day, hour, version):
    """Get initialisation time and forecast offset from
    analysis validity time."""
    dte = datetime.datetime(year, month, day, int(hour))
    if variable in monolevel_analysis or variable in multilevel_analysis:
        if hour % 6 == 0:
            ic_time = iris.time.PartialDateTime(
                year=dte.year, month=dte.month, day=dte.day, hour=dte.hour
            )
            fc_time = 0
        elif hour % 3 == 0:
            dte = dte - datetime.timedelta(hours=3)
            ic_time = iris.time.PartialDateTime(
                year=dte.year, month=dte.month, day=dte.day, hour=dte.hour
            )
            fc_time = 3
        else:
            raise Exception(
                "Unsupported validity time %s" % dte.strftime("%Y-%m-%d:%H:%M:%S%z")
            )
    elif variable in monolevel_forecast:
        if hour % 6 == 0:
            dte = dte - datetime.timedelta(hours=6)
            ic_time = iris.time.PartialDateTime(
                year=dte.year, month=dte.month, day=dte.day, hour=dte.hour
            )
            fc_time = 6
        elif hour % 3 == 0:
            dte = dte - datetime.timedelta(hours=3)
            ic_time = iris.time.PartialDateTime(
                year=dte.year, month=dte.month, day=dte.day, hour=dte.hour
            )
            fc_time = 3
        else:
            raise Exception(
                "Unsupported validity time %s" % dte.strftime("%Y-%m-%d:%H:%M:%S%z")
            )
    else:
        raise Exception("Unsupported variable %s" % variable)
    return {"initial": ic_time, "offset": fc_time}


def _get_slice_at_hour_at_timestep(
    variable, year, month, day, hour, height, level, ilevel, version
):
    """Get the cube with the data, given that the specified time
    matches a data timestep."""
    if not _is_in_file(variable, hour):
        raise ValueError("Invalid hour - data not in file")
    file_name = _get_data_file_name(
        variable, year, month, height, level, ilevel, version
    )
    file_times = _time_to_time(variable, year, month, day, hour, version)
    ic_constraint = iris.Constraint(
        coord_values={"initial time": lambda x: x == file_times["initial"]}
    )
    fc_constraint = iris.Constraint(
        coord_values={
            "Forecast offset from initial time": lambda x: x == file_times["offset"]
        }
    )
    try:
        with warnings.catch_warnings():  # Iris is v.fussy
            warnings.simplefilter("ignore")
            hslice = iris.load_cube(file_name, ic_constraint & fc_constraint)
    except iris.exceptions.ConstraintMismatchError:
        raise Exception(
            "%s not available for %04d-%02d-%02d:%02d"
            % (variable, year, month, day, hour)
        )

    # Enhance the names and metadata for iris/cartopy
    hslice.coord("latitude").coord_system = coord_s
    hslice.coord("longitude").coord_system = coord_s
    hslice.dim_coords[0].rename("member")  # Remove spaces in name
    # Need a validity time dimension for interpolation
    hslice.coord("initial time").rename("time")
    hslice.coord("time").points = (
        hslice.coord("time").points
        + hslice.coord("Forecast offset from initial time").points
    )
    return hslice


def load(variable, dtime, height=None, level=None, ilevel=None, version="5.7.6"):
    """Load requested data from disc, interpolating if necessary.

    Data must be available in directory $SCRATCH/20CR, previously retrieved by :func:`fetch`.

    Args:
        variable (:obj:`str`): Variable to fetch (e.g. 'prmsl')
        height (:obj:`int`): Height above ground (m) for 3d variables. Variable must be in 20CR output at that exact height (no interpolation). Defaults to None - appropriate for 2d variables.
        level (:obj:`int`): Pressure level (hPa) for 3d variables. Variable must be in 20CR output at that exact pressure level (no interpolation). Defaults to None - appropriate for 2d variables.
        ilevel (:obj:`int`): Isentropic level (K) for 3d variables. Variable must be in 20CR output at that exact pressure level (no interpolation). Defaults to None - appropriate for 2d variables.
        dtime (:obj:`datetime.datetime`): Date and time to load data for.

    Returns:
        :obj:`iris.cube.Cube`: Global field of variable at time.

    Note that 20CR data is only output every 3 hours, so if hour%3!=0, the result may be linearly interpolated in time.

    Raises:
        StandardError: Data not on disc - see :func:`fetch`

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
            height,
            level,
            ilevel,
            version,
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
        height,
        level,
        ilevel,
        version,
    )
    s_next = _get_slice_at_hour_at_timestep(
        variable,
        next_step["year"],
        next_step["month"],
        next_step["day"],
        next_step["hour"],
        height,
        level,
        ilevel,
        version,
    )
    # Iris won't merge cubes with different attributes
    s_previous.attributes = s_next.attributes
    s_next = iris.cube.CubeList((s_previous, s_next)).merge_cube()
    s_next = s_next.interpolate([("time", dt_current)], iris.analysis.Linear())
    return s_next
