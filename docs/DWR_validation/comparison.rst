Validation Spread v. Error plot January 1872 + Spring 1903 + February 1953
==========================================================================

.. figure:: ../../analyses/DWR_validation/case_studies/intercomparison/E_v_E.png
   :width: 95%
   :align: center
   :figwidth: 95%

   RMS reanalysis difference from observations, against reanalysis spread. For three reanalyses: 20CR2c in black, 20CR3 in red, and CERA-20C in blue. 

The comparison includes data from three months of January to March 1903, augmented by January 1872 (higher spread) and Febriuary 1953 (lower spread).

If the observations were perfect, and the reanalysis spread was an unbiased estimate of its error, the RMS difference and the spread would be the same at all points. Because the observations have error, the RMS difference should be bigger than the spread, especially at small spread: the three grey lines show the expected relationship for three values of observation error (0, 1 and 2hPa). If the points are above the lines, the reanalysis is overconfident (spread too small) - if they are below the lines it is underconfident (spread too large).

|

First make the equivalent figure for each period seperately:

* :doc:`January 1872 <January_1872/comparison>`
* :doc:`Spring 1903 <Spring_1903/comparison>`
* :doc:`February 1953 <February_1953/comparison>`

Then make the figure

.. literalinclude:: ../../analyses/DWR_validation/case_studies/intercomparison/rms_v_rms.py
