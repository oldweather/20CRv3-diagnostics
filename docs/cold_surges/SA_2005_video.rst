:orphan:

South American cold surge of 2005 video
=======================================

.. raw:: html

    <center>
    <table><tr><td><center>
    <iframe src="https://player.vimeo.com/video/303321991?title=0&byline=0&portrait=0" width="795" height="448" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe></center></td></tr>
    <tr><td><center>MSLP contours and 850hPa temperature field from 20CRv2c (left) and 20CRv3 (right)</center></td></tr>
    </table>
    </center>

The thin lines are MSLP contours from each of 56 ensemble members. The thicker lines are contours of the ensemble mean. The background colour field shows the ensemble mean temperature at 850hPa. The small circles mark pressure observations assimilated while making the fields shown.

|

Code to make the figure
-----------------------

Download the data required:

.. literalinclude:: ../../analyses/cold_surges/Argentina_September_2005/get_data.py

Script to make an individual frame - takes year, month, day, and hour as command-line options:

.. literalinclude:: ../../analyses/cold_surges/Argentina_September_2005/video/CS_V3vV2c.py

To make the video, it is necessary to run the script above hundreds of times - giving an image for every 15-minute period. This script makes the list of commands needed to make all the images, which can be run `in parallel <http://brohan.org/offline_assimilation/tools/parallel.html>`_.

.. literalinclude:: ../../analyses/cold_surges/Argentina_September_2005/video/make_frames.py

To turn the thousands of images into a movie, use `ffmpeg <http://www.ffmpeg.org>`_

.. code-block:: shell

    ffmpeg -r 24 -pattern_type glob -i SA_cold_surge_2005/\*.png \
           -c:v libx264 -threads 16 -preset slow -tune animation \
           -profile:v high -level 4.2 -pix_fmt yuv420p -crf 25 \
           -c:a copy SA_cold_surge_2005.mp4
