CERA-20C compared with new observations in Spring 1903 (video)
==============================================================

.. seealso:: * :doc:`Still image version <scatter+contour>`
             * :doc:`Validation scatterplot <scatterplot>`
             * :doc:`Spread v. Error plot <rms_v_rms>`

.. topic:: Compare

    .. list-table::
	:widths: 35 45 45 45
	:header-rows: 0  

	* - 20CR2c
	  - :doc:`January 1872 <../../January_1872/20cr2c/scatter+contour_video>`
	  - :doc:`Spring 1903 <../../Spring_1903/20cr2c/scatter+contour_video>`
	  - :doc:`February 1953 <../../February_1953/20cr2c/scatter+contour_video>`
	* - 20CR3
	  - :doc:`January 1872 <../../January_1872/20cr3/scatter+contour_video>`
	  - :doc:`Spring 1903 <../../Spring_1903/20cr3/scatter+contour_video>`
	  - :doc:`February 1953 <../../February_1953/20cr3/scatter+contour_video>`
	* - CERA-20C
	  - 
	  - :doc:`Spring 1903 <../../Spring_1903/CERA-20C/scatter+contour_video>`
	  - :doc:`February 1953 <../../February_1953/CERA-20C/scatter+contour_video>`
 
.. raw:: html

    <center>
    <table><tr><td><center>
    <iframe src="https://player.vimeo.com/video/282649119?title=0&byline=0&portrait=0" width="795" height="448" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe></center></td></tr>
    <tr><td><center>MSLP contours (left) and value at the new station locations (right)<br></center></td></tr>
    </table>
    </center>

Left panel is a spaghetti-contour plot of reanalysis mean-sea-level pressure. The grey dots mark the new stations used for validation.

Right panel shows the observed MSLP (red line) and the reanalysis ensemble values (blue dots) at the station location, for each new station. 

|

Download the data (uses :doc:`this script <../../scripts/get_data>`)

.. literalinclude:: ../../../../analyses/DWR_validation/case_studies/Spring_1903/CERA20C/get_data.sh
   :language: sh

To make the video, it is necessary to run :doc:`this script <../../scripts/scatter+contour>` hundreds of times - giving an image for every 15-minute period. The best way to do this is system dependent - the script below does it on the Met Office SPICE cluster - it will need modification to run on any other system. (Could do this on a single PC, but it will take many hours).

.. literalinclude:: ../../../../analyses/DWR_validation/case_studies/Spring_1903/CERA20C/video/make_frames.py

To turn the thousands of images into a movie, use `ffmpeg <http://www.ffmpeg.org>`_

.. code-block:: shell

    ffmpeg -r 24 -pattern_type glob -i vcs_cera20c_1903_scatter+contour/\*.png \
           -c:v libx264 -threads 16 -preset slow -tune animation \
           -profile:v high -level 4.2 -pix_fmt yuv420p -crf 25 \
           -c:a copy vcs_cera20c_1903_scatter+contour.mp4
