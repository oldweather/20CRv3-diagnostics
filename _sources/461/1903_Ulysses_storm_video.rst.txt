:orphan:

Ulysses storm (1903) video with the weatherrescue.org observations
==================================================================

.. raw:: html

    <center>
    <table><tr><td><center>
    <iframe src="https://player.vimeo.com/video/338221700?title=0&byline=0&portrait=0" width="795" height="448" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe></center></td></tr>
    <tr><td><center>MSLP Contours for v3 (left) and scout 4.6.1 (right)</center></td></tr>
    </table>
    </center>

The black lines are contours of the ensemble mean. The green shading shows the uncertainty in each contour - the amount of shading shows the probability there is a contour at each location (estimated from the reanalysis ensemble). The yellow dots mark pressure observations assimilated while making the field shown.

|

The new observations in scout 4.6.1 come from  `weatherrescue.org <https://weatherrescue.wordpress.com/2017/10/12/february-1903-the-ulysses-storm/>`_.

Download the data required:

.. literalinclude:: ../../analyses/4.6.1/Ulysses_storm_1903/get_data.py

Script to make an individual frame - takes year, month, day, and hour as command-line options:

.. literalinclude:: ../../analyses/4.6.1/Ulysses_storm_1903/video/US_V3v461.py

To make the video, it is necessary to run the script above hundreds of times - giving an image for every 15-minute period. This script makes the list of commands needed to make all the images, which can be run `in parallel <http://brohan.org/offline_assimilation/tools/parallel.html>`_.

.. literalinclude:: ../../analyses/4.6.1/Ulysses_storm_1903/video/make_frames.py

To turn the thousands of images into a movie, use `ffmpeg <http://www.ffmpeg.org>`_

.. code-block:: shell

    ffmpeg -r 24 -pattern_type glob -i Ulyses_storm/\*.png \
           -c:v libx264 -threads 16 -preset slow -tune animation \
           -profile:v high -level 4.2 -pix_fmt yuv420p -crf 25 \
           -c:a copy Ulysses_storm.mp4
