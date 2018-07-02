Extracting data from 20CRv3
===========================

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

Look for the scripts in directory '/global/homes/p/pbrohan/Projects/20CRv3-diagnostics/extract_data/' (or `clone this repository <https://github.com/oldweather/20CRv3-diagnostics>`_).

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

Strip output for one variable and convert to netCDF
---------------------------------------------------

There are two different sorts of variables in 20CR - analysis variables and forecast variables:

Analysis variables are obtained from the 'pgrbanl' files. For the grib2 data, the :doc:`script that extracts and converts them <release_extract_anl_var>` is called as:

.. code-block:: bash

    v3_release/extract_anl_var.py --startyear=1899 --year=1903 --month=10 --version=451 --var=prmsl

--var must be one of 'prmsl', 'air.2m', 'uwnd.10m', 'vwnd.10m', 'air.sfc', and 'icec'.

Forecast variables are obtained from the 'pgrbanl' and 'pgrbfg' files. For the grib2 data, the :doc:`script that extracts and converts them <release_extract_fg_var>` is called as:

.. code-block:: bash

    v3_release/extract_fg_var.py --startyear=1899 --year=1903 --month=10 --version=451 --var=prate

only --var=prate is currently supported.

For the grib1 data the calls are exactly the same (:doc:`analysis <orig_extract_anl_var>`, :doc:`forecast <orig_extract_fg_var>`), but the scripts are in the 'v3_orig' directory.

Whatever the original format, these scripts will create output files of the form '$SCRATCH/20CRv3.final/version_4.5.1/1903/10/prmsl.nc' which are netCDF files similar to those from v2c.

These scripts will also take some time to run (at least 2 hours).

Assemble the observations files
-------------------------------

The observations feedback files are text files (the the format is different to v2c), so it's just a matter of copying them to the output directory. The :doc:`script to do that (for the grib2 data) <release_extract_obs>` is called as:

.. code-block:: bash

    v3_release/extract_obs.py --startyear=1899 --year=1903 --month=10 --version=451

and the :doc:`analagous script for grib1 <orig_extract_obs>` is in directory v3_orig. Either of these will copy all the observations files to '$SCRATCH/20CRv3.final/version_4.5.1/1903/10/observations'. 

These scripts only take a couple of minutes to run.

ToDo
----

These scripts work fine, but the process is fiddly and slow. An obvious improvement is to write a single script that automatically detects the data source, and then runs a sequence of jobs to do the extraction, working in parallel where possible. I failed at this, as running multiple extractions in parallel makes them **very** slow (possibly because of file-system contention). Some cunning will be necessary to produce an efficient script, and so far I have not bothered.
