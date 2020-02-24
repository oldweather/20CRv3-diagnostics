20CRv3 Diagnostics
==================

This is a set of analyses of the newly-released `NOAA/CIRES/DOE Twentieth Century Reanalysis <https://www.esrl.noaa.gov/psd/data/20thC_Rean/>`_ version 3 (20CRv3). It compares `20CRv3 <https://www.esrl.noaa.gov/psd/data/gridded/data.20thC_ReanV3.html>`_ to `20CRv2c <https://www.esrl.noaa.gov/psd/data/gridded/data.20thC_ReanV2c.html>`_, to `CERA-20C <https://www.ecmwf.int/en/forecasts/datasets/archive-datasets/reanalysis-datasets/cera-20c>`_, and to `newly-digitised observations from around the British Isles <https://oldweather.github.io/DWR/>`_.

Get the data
------------

The 20CRv3 data used here is distributed through the `NERSC web portal <https://portal.nersc.gov/archive/home/projects/incite11/www>`_. It can be downloaded directly.

Data from scout runs can be obtained (with some effort) by :doc:`following these instructions <extract_data/extract_data>`.

Stripes plots
-------------

Latitude:time plots of monthly averages.

.. toctree::
   :maxdepth: 1

   TMP2m <stripes/TMP2m/index> 
   PRMSL <stripes/PRMSL/index>


Comparisons of 20CRv3 with 20CRv2c
----------------------------------

.. toctree::
   :maxdepth: 2

   tropical-storms/tropical_storms
   european_windstorms/european_windstorms
   extreme_months/extreme_months
   north_american_severe_weather/nasw
   australian_east_coast_lows/aecl
   cold_surges/cold_surges
   

Validation against observations
-------------------------------

The `new observations rescued from the Daily Weather Reports <https://oldweather.github.io/DWR/>`_ have not yet been used by any reanalysis, so they are ideal for validation. Doing the comparison for several different times during the period covered by the new observations shows the effect of varying reanalysis and observation quality.

.. toctree::
   :maxdepth: 1

   DWR_validation/January_1872/january_1872.rst
   DWR_validation/Spring_1903/spring_1903.rst
   DWR_validation/February_1953/february_1953.rst
   DWR_validation/comparison

Observations and fog videos
---------------------------

.. toctree::
   :maxdepth: 1

   obs_video/obs_video.rst
   fog_videos/1903
   fog_videos/1931
   fog_videos/1880_Arctic


Small print
-----------

.. toctree::
   :maxdepth: 1

   Authors and acknowledgements <credits>

This document and the data associated with it, are crown copyright (2018) and distributed under the terms of the `Open Government Licence <https://www.nationalarchives.gov.uk/doc/open-government-licence/version/2/>`_. All code included is licensed under the terms of the `GNU Lesser General Public License <https://www.gnu.org/licenses/lgpl.html>`_.
