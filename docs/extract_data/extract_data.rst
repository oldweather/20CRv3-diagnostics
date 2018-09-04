Extracting data from 20CRv3
===========================

Executive summary
-----------------

On `Cori <http://www.nersc.gov/users/computational-systems/cori/>`_, from an account that's part of the 20CR group, run:

.. code-block:: bash

   /global/homes/p/pbrohan/Projects/20CRv3-diagnostics/tools/extract_data/v3_release/extract_month_job.py --startyear=1899 --year=1901 --month=7 --version=451

(But change 1899, 1901, 7, and possibly 451, to your preferred values).

This will make a netCDF4 file, for each of the surface weather variables ``prmsl``, ``air.2m``, ``uwnd.10m``, ``vwnd.10m``, ``icec``, and ``prate``, containing the 3-hourly, full ensemble, analysis output for the whole of July 1901, from the experiment 451 run starting in 1899. It will also extract the observations feedback files. It will put the output in ``$SCRATCH/20CRv3.final/``

The command will submit an `xfer job <http://www.nersc.gov/users/computational-systems/cori/running-jobs/advanced-running-jobs-options/>`_ to get the data off tape, and when that's done it will submit a regular job to do the data reshaping and conversion. This will take a while - a minimum of all day, and longer if the system is heavily loaded. You can run multiple extractions in parallel - if you submit more than Cori can run at once, they will just queue up.

The details
-----------

The 20CRv2c data are `available <http://portal.nersc.gov/project/20C_Reanalysis/>`_ as netCDF files, each containing 3- or 6-hourly data, for a single variable, for all ensemble members, for a year. I have `software that uses data in this format <https://brohan.org/IRData>`_, so I aim to produce v3 data in a similar format. The main difference is that there is much more data from v3 (higher resolution, more ensemble members, always 3-hourly) so I make files for each month, not each year.

v3 does not exist yet, we identify proto-v3 data by its *run number*. The two run numbers I've looked at so far are 451 and 452. Run numbers in the 400s are from the v3 model and this data extraction method should work for any of them.

The data extraction process is in four steps:

1. Find the model output files for a month
2. Copy them to my own $SCRATCH
3. Copy all the output for a single variable to one grib file and convert it to netCDF
4. Assemble the observations files

Setup
-----

All the scripts need to be run on `Cori <http://www.nersc.gov/users/computational-systems/cori/>`_, from an account that's part of the 20CR group.
The conversion scripts use the NCAR library and the netcdf operators, these need to be loaded as modules:

.. code-block:: bash

   module load ncar
   module load nco

The data extraction scripts use `wgrib2 <http://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/>`_ and by default this will use all the cores on the system it is running on, in an attempt to go faster. If you are using a (shared) login node, this is not what you want (and will get you shouted at by the sysops). Tell it to only use one core:

.. code-block:: bash

   export OMP_NUM_THREADS=1

(If you are running the scripts in a job, on a dedicated node, you may get a useful speedup by setting this to a larger number).

Look for the scripts in directory '/global/homes/p/pbrohan/Projects/20CRv3-diagnostics/tools/extract_data/' (or `clone this repository <https://github.com/oldweather/20CRv3-diagnostics>`_).

Find the model output files
---------------------------

The model output for a single assimilation step (6-hour period) is all put in the same directory, with a name formated as YYYYMMDDHH, so directory 1928031206 contains data for the 6-hour period starting at 6a.m (UTC) on March 12 1928. There are 4 assimilation steps each day (0,6,12,18 hours). The analysis is run in many streams (usually of 5-years duration) - a different stream is started every 5 years. So the model outputs are uniquely identified by their *run number*, their *start year*, and their *date*: directory 'ensda_451_1899/1903102618' contains the data for run 451, stream starting in 1899, valid at 6pm UTC on 26 October 1903.

The freshest model output is in the $SCRATCH directory of whoever is doing the run (Chesley or Gil):

* /global/cscratch1/sd/cmccoll/gfsenkf_20crV3_cmip5oz_CoriII/
* /global/cscratch1/sd/compo/gfsenkf_20crV3_cmip5oz_CoriII/

But there is too much output to keep on disc for long, so the output is put into tar files by date, and `archived to tape <http://www.nersc.gov/users/storage-and-file-systems/hpss/storing-and-retrieving-data/clients/hsi-usage/>`_ in hsi directory:

* /home/projects/incite11/ensda_v451_archive_orig

where '451' is the run number.

This data in turn is then cleaned-up, repacked into grib2 format, and copied into another tape archive at 

* /home/projects/incite11/ensda_v451_archive_grb2_monthly

In practice it's best to use these in reverse order: If the month you want is in the grib2 tape archive, get it from there; otherwise if it's in the grib1 tabe archive, get it from there; only look on disc if you must have data that's currently being run.

Copy to my own $SCRATCH
-----------------------

If the data are in the grib2 tape archive, copy them to '$SCRATCH/20CR_working/ensda_1899/1903/10' (where 1899, 1903, and 10 are replaced by start year, validity year, and validity month). The :doc:`script to do this <release_month_from_tape>` is called as:

.. code-block:: bash

    v3_release/month_from_tape.py --startyear=1899 --year=1903 --month=10 --version=451

If the data are not yet in the grib2 archive, but they are in the hsi grib1 archive, then copy them to '$SCRATCH/20CR_working_orig/ensda_1899/1903/10' (replacing start year, validity year, and validity month, as appropriate). The :doc:`script to do this <orig_month_from_tape>` is called with the same options as above:

.. code-block:: bash

    v3_orig/month_from_tape.py --startyear=1899 --year=1903 --month=10 --version=451

If the data are not yet on tape, only on disc, then they are in grib1 format - copy them directly ('cp' command) into the grib1 working directory: '$SCRATCH/20CR_working_orig/ensda_1899/1903/10' (replacing start year, validity year, and validity month, as appropriate).

In all cases the data transfer will take several hours.

A full month's 20CR output is a *lot* of data, and if you do this data extraction for more than a couple of months you will exceed your allocation on SCRATCH (and be shouted at by the sysops). Once you've done the data extraction (below) it's a good idea to clean out '$SCRATCH/20CR_working' and '$SCRATCH/20CR_working_orig'

Strip output for one variable and convert to netCDF
---------------------------------------------------

There are two different sorts of variables in 20CR - analysis variables and forecast variables:

Analysis variables are obtained from the 'pgrbanl' files. For the grib2 data, the :doc:`script that extracts and converts them <release_extract_anl_var>` is called as:

.. code-block:: bash

    v3_release/extract_anl_var.py --startyear=1899 --year=1903 --month=10 --version=451 --var=prmsl

--var must be one of 'prmsl', 'air.2m', 'uwnd.10m', 'vwnd.10m', 'air.sfc', and 'icec'. If you want anything else you will have to edit the script (please send a `pull request <http://oss-watch.ac.uk/resources/pullrequest>`_ with your improved version).

Forecast variables are obtained from the 'pgrbanl' and 'pgrbfg' files. For the grib2 data, the :doc:`script that extracts and converts them <release_extract_fg_var>` is called as:

.. code-block:: bash

    v3_release/extract_fg_var.py --startyear=1899 --year=1903 --month=10 --version=451 --var=prate

only --var=prate is currently supported.

For the grib1 data the calls are exactly the same (:doc:`analysis <orig_extract_anl_var>`, :doc:`forecast <orig_extract_fg_var>`), but the scripts are in the 'v3_orig' directory.

Whatever the original format, these scripts will create output files of the form '$SCRATCH/20CRv3.final/version_4.5.1/1903/10/prmsl.nc' which are netCDF files similar to those from v2c.

These scripts will also take some time to run (at least 2 hours).

Assemble the observations files
-------------------------------

The observations feedback files are text files (though the format is different to v2c), so it's just a matter of copying them to the output directory. The :doc:`script to do that (for the grib2 data) <release_extract_obs>` is called as:

.. code-block:: bash

    v3_release/extract_obs.py --startyear=1899 --year=1903 --month=10 --version=451

and the :doc:`analagous script for grib1 <orig_extract_obs>` is in directory v3_orig. Either of these will copy all the observations files to '$SCRATCH/20CRv3.final/version_4.5.1/1903/10/observations'. 

These scripts only take a couple of minutes to run.

Optimisation
------------

You can run all these scripts in sequence on a login node, and it will work fine, but it's a hassle, and performance is variable depending on system load. A simpler aproach is to submit jobs to do the work, and this can be much faster as the extractions can be run in parallel.

First, submit an xfer job to get the data off tape. The :doc:`script to do that <from_tape_job>` is:

.. code-block:: bash

    extract_month_job.py --startyear=1899 --year=1903 --month=10 --version=451

When that job has completed, it will submit a follow-on regular job to extract and convert the data. The :doc:`script it runs to do that <conversion_job>` is:

.. code-block:: bash

    conversion_job.py --startyear=1899 --year=1903 --month=10 --version=451

which wil extract and convert all the standard surface variables. As it uses so few resources, it will usually start running soon after being submitted, but this depends on the system load and the job queue. When the conversion completes, it will delete all the tape retrievals from SCRATCH.

These two scripts only work for grib2 data
