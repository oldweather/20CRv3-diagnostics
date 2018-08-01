Validation Spread v. Error plot Spring 1903
===========================================

.. figure:: ../../../analyses/DWR_validation/case_studies/Spring_1903/intercomparison/E_v_E.png
   :width: 650px
   :align: center
   :figwidth: 700px

   RMS reanalysis difference from observations, against reanalysis spread. For three reanalyses: 20CR2c in black, 20CR3 in red, and CERA-20C in blue. 

The comparison covers the three months of January to March 1903.

If the observations were perfect, and the reanalysis spread was an unbiased estimate of its error, the RMS difference and the spread would be the same at all points. Because the observations have error, the RMS difference should be bigger than the spread, especially at small spread: the three grey lines show the expected relationship for three values of observation error (0, 1 and 2hPa). If the points are above the lines, the reanalysis is overconfident (spread too small) - if they are below the lines it is underconfident (spread too large).

|

First make the equivalent figure for each reanalysis seperately:

* :doc:`20CR2c <20cr2c/rms_v_rms>`
* :doc:`20CR3 <20cr3/rms_v_rms>`
* :doc:`CERA-20C <CERA-20C/rms_v_rms>`

Then make the figure

.. literalinclude:: ../../../analyses/DWR_validation/case_studies/Spring_1903/intercomparison/rms_v_rms.py
