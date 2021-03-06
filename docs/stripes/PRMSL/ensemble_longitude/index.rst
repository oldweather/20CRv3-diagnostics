:orphan:

PRMSL ensemble stripes by longitude
===================================

.. seealso:: 
   :doc:`Full ensemble by latitude <../index>`

   :doc:`Ensemble mean by latitude <../ensemble_mean/index>`

   :doc:`Single member by latitude <../single_member/index>`

.. figure:: ../../../../analyses/stripes/PRMSL/ensemble_longitude/PRMSL.png
   :width: 95%
   :align: center
   :figwidth: 95%

   Monthly mean-sea-level pressure anomalies (w.r.t. 1961-90) from the 20CRv3 ensemble. The vertical axis is longitude, and each pixel is an area-weighted latitudinal mean from a randomly selected ensemble member.

Sampling randomly from the ensemble means that regions where the variance across the ensemble is larger than the ensemble mean appear speckled. This provides an indication of uncertainty.

.. toctree::
   :titlesonly:
   :maxdepth: 1

   Script to download the data <./data.rst>
   Scripts to make the plot <./plot.rst>
   Function to extract the data sample <./sample.rst>
