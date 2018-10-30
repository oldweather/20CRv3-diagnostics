Christmas Storm of 1811
=======================

.. seealso:: :doc:`Video version <1811_Xmas_storm_video>`

.. figure:: ../../analyses/european_windstorms/xmas_eve_1811/V3only_x11_1811122312.png
   :width: 95%
   :align: center
   :figwidth: 95%

   MSLP for v3 (right) - there is no v2c data for 1811.

   The thin blue lines are mslp contours from the first 56 ensemble members . The thicker black lines are contours of the ensemble mean. The yellow dots mark pressure observations assimilated while making the field shown. 

|

The `Christmas storm of 1811 <https://ageofsail.wordpress.com/2009/04/24/the-christmas-gale-of-1811/>`_ Drove HMS Defence, HMS St George, HMS Hero, and HMS Grasshopper aground on Jutland: more than 1,900 sailors were killed.

This means strong north-west winds in the north sea, and implies a deep low over scandinavia. The uncertainties are large, which reduces the amplitude of the ensemble mean signal, but 20CRv3 does reproduce this feature.

|

Code to make the figure
-----------------------

Download the data required:

.. literalinclude:: ../../analyses/european_windstorms/xmas_eve_1811/get_data.py

Make the figure:

.. literalinclude:: ../../analyses/european_windstorms/xmas_eve_1811/x11_V3only.py

