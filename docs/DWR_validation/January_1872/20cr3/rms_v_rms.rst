20CR3 validation Spread v. Error plot January 1872
==================================================

.. seealso:: * :doc:`Video contourplot <scatter+contour_video>`
             * :doc:`Still contourplot <scatter+contour>`
             * :doc:`Validation scatterplot <scatterplot>`

.. topic:: Compare

    .. list-table::
	:widths: 35 45 45 45
	:header-rows: 0  

	* - 20CR2c
	  - :doc:`January 1872 <../../January_1872/20cr2c/rms_v_rms>`
	  - :doc:`Spring 1903 <../../Spring_1903/20cr2c/rms_v_rms>`
	  - :doc:`February 1953 <../../February_1953/20cr2c/rms_v_rms>`
	* - 20CR3
	  - :doc:`January 1872 <../../January_1872/20cr3/rms_v_rms>`
	  - :doc:`Spring 1903 <../../Spring_1903/20cr3/rms_v_rms>`
	  - :doc:`February 1953 <../../February_1953/20cr3/rms_v_rms>`
	* - CERA-20C
	  - 
	  - :doc:`Spring 1903 <../../Spring_1903/CERA-20C/rms_v_rms>`
	  - :doc:`February 1953 <../../February_1953/CERA-20C/rms_v_rms>`
 
.. figure:: ../../../../analyses/DWR_validation/case_studies/January_1872/20CRv3/E_v_E_1872-01-02_to_1872-02-01_20cr3.png
   :width: 650px
   :align: center
   :figwidth: 700px

   RMS reanalysis difference from observations, against reanalysis spread.

If the observations were perfect, and the reanalysis spread was an unbiased estimate of its error, the RMS difference and the spread would be the same at all points. Because the observations have error, the RMS difference should be bigger than the spread, especially at small spread: the three grey lines show the expected relationship for three values of observation error (0, 1 and 2hPa). If the points are above the lines, the reanalysis is overconfident (spread too small) - if they are below the lines it is underconfident (spread too large).

|

Download the data (uses :doc:`this script <../../scripts/get_data>`)

.. literalinclude:: ../../../../analyses/DWR_validation/case_studies/January_1872/20CRv3/get_data.sh
   :language: sh

Extract the reanalysis data associated with each observation (uses :doc:`this script <../../scripts/get_comparison>`)

.. literalinclude:: ../../../../analyses/DWR_validation/case_studies/January_1872/20CRv3/get_comparison.sh
   :language: sh

Make the figure (uses :doc:`this script <../../scripts/rms_v_rms>`)

.. literalinclude:: ../../../../analyses/DWR_validation/case_studies/January_1872/20CRv3/rms_v_rms.sh
   :language: sh
