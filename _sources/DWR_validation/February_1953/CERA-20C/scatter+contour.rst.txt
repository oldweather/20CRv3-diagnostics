CERA-20C compared with new observations in February 1953
========================================================

.. seealso:: * :doc:`Video version <scatter+contour_video>`
             * :doc:`Validation scatterplot <scatterplot>`
             * :doc:`Spread v. Error plot <rms_v_rms>`

.. topic:: Compare

    .. list-table::
	:widths: 35 45 45 45
	:header-rows: 0  

	* - 20CR2c
	  - :doc:`January 1872 <../../January_1872/20cr2c/scatter+contour>`
	  - :doc:`Spring 1903 <../../Spring_1903/20cr2c/scatter+contour>`
	  - :doc:`February 1953 <../../February_1953/20cr2c/scatter+contour>`
	* - 20CR3
	  - :doc:`January 1872 <../../January_1872/20cr3/scatter+contour>`
	  - :doc:`Spring 1903 <../../Spring_1903/20cr3/scatter+contour>`
	  - :doc:`February 1953 <../../February_1953/20cr3/scatter+contour>`
	* - CERA-20C
	  - 
	  - :doc:`Spring 1903 <../../Spring_1903/CERA-20C/scatter+contour>`
	  - :doc:`February 1953 <../../February_1953/CERA-20C/scatter+contour>`
 
.. figure:: ../../../../analyses/DWR_validation/case_studies/February_1953/CERA20C/Scatter+contour_195302101800.png
   :width: 95%
   :align: center
   :figwidth: 95%

   MSLP contours (left) and at the new station locations (right)

   Left panel is a spaghetti-contour plot of reanalysis mean-sea-level pressure. The grey dots mark the new stations used for validation.

   Right panel shows the observed MSLP (red line) and the reanalysis ensemble values (blue dots) at the station location, for each new station. 

|

Download the data (uses :doc:`this script <../../scripts/get_data>`)

.. literalinclude:: ../../../../analyses/DWR_validation/case_studies/February_1953/CERA20C/get_data.sh
   :language: sh

Make the figure (uses :doc:`this script <../../scripts/scatter+contour>`)

.. literalinclude:: ../../../../analyses/DWR_validation/case_studies/February_1953/CERA20C/scatter+contour.sh
   :language: sh
