CERA-20C validation scatterplot Spring 1903
===========================================

.. seealso:: * :doc:`Video contourplot <scatter+contour_video>`
             * :doc:`Still contourplot <scatter+contour>`
             * :doc:`Spread v. Error plot <rms_v_rms>`

.. topic:: Compare

    .. list-table::
	:widths: 35 45 45 45
	:header-rows: 0  

	* - 20CR2c
	  - :doc:`January 1872 <../../January_1872/20cr2c/scatterplot>`
	  - :doc:`Spring 1903 <../../Spring_1903/20cr2c/scatterplot>`
	  - :doc:`February 1953 <../../February_1953/20cr2c/scatterplot>`
	* - 20CR3
	  - :doc:`January 1872 <../../January_1872/20cr3/scatterplot>`
	  - :doc:`Spring 1903 <../../Spring_1903/20cr3/scatterplot>`
	  - :doc:`February 1953 <../../February_1953/20cr3/scatterplot>`
	* - CERA-20C
	  - 
	  - :doc:`Spring 1903 <../../Spring_1903/CERA-20C/scatterplot>`
	  - :doc:`February 1953 <../../February_1953/CERA-20C/scatterplot>`
 
.. figure:: ../../../../analyses/DWR_validation/case_studies/Spring_1903/CERA20C/Scatter_1903-01-02_to_1903-04-01_cera.png
   :width: 95%
   :align: center
   :figwidth: 95%

   Scatterplot of observed v. reanalysis MSLP

|

Download the data (uses :doc:`this script <../../scripts/get_data>`)

.. literalinclude:: ../../../../analyses/DWR_validation/case_studies/Spring_1903/CERA20C/get_data.sh
   :language: sh

Extract the reanalysis data associated with each observation (uses :doc:`this script <../../scripts/get_comparison>`)

.. literalinclude:: ../../../../analyses/DWR_validation/case_studies/Spring_1903/CERA20C/get_comparison.sh
   :language: sh

Make the figure (uses :doc:`this script <../../scripts/scatter>`)

.. literalinclude:: ../../../../analyses/DWR_validation/case_studies/Spring_1903/CERA20C/plot_scatter.sh
   :language: sh
