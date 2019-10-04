Observations coverage video
===========================

.. raw:: html

    <center>
    <table><tr><td><center>
    <iframe src="https://player.vimeo.com/video/364280156?title=0&byline=0&portrait=0" width="795" height="448" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe></center></td></tr>
    <tr><td><center>Locations with observations</center></td></tr>
    </table>
    </center>

In each 1x1 degree grid-cell, a bright yellow circle is shown if at least one pressure observation is available every 6 hours (one in each assimilation run). Paler yellow circles indicate observations in some, but not all assimilation periods (partial coverage). Each frame covers a 10-day period. 

|

Code to make the figure
-----------------------


Script to make an individual frame - takes year, month, day, and hour as command-line options:

.. literalinclude:: ../../analyses/obs_video/plot_obs_coverage.py

To make the video, it is necessary to run the script above hundreds of times - giving an image for every 10-day period. This script makes the list of commands needed to make all the images, which can be run `in parallel <http://brohan.org/offline_assimilation/tools/parallel.html>`_.

.. literalinclude:: ../../analyses/obs_video/make_frames.py

To turn the thousands of images into a movie, use `ffmpeg <http://www.ffmpeg.org>`_

.. code-block:: shell

    ffmpeg -r 24 -pattern_type glob -i 20CRv3_observations/\*.png \
           -c:v libx264 -threads 16 -preset veryslow -tune film \
           -profile:v high -level 4.2 -pix_fmt yuv420p \
           -b:v 5M -maxrate 5M -bufsize 20M \
           -c:a copy 20CRv3_observations.mp4
