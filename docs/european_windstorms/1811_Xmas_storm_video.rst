:orphan:

Christmas Storm of 1811 video
=============================

.. raw:: html

    <center>
    <table><tr><td><center>
    <iframe src="https://player.vimeo.com/video/297927607?title=0&byline=0&portrait=0" width="795" height="448" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe></center></td></tr>
    <tr><td><center>MSLP for v3 (right) - there is no v2c data for 1811</center></td></tr>
    </table>
    </center>

The thin blue lines are mslp contours from the first 56 ensemble members . The thicker black lines are contours of the ensemble mean. The yellow dots mark pressure observations assimilated while making the field shown.
|

The `Christmas storm of 1811 <https://ageofsail.wordpress.com/2009/04/24/the-christmas-gale-of-1811/>`_ Drove HMS Defence, HMS St George, HMS Hero, and HMS Grasshopper aground on Jutland (on Dec 24th): more than 1,900 sailors were killed.

This means strong north-west winds in the north sea, and implies a deep low over scandinavia. The uncertainties are large, which reduces the amplitude of the ensemble mean signal, but 20CRv3 does reporoduce this feature.

Download the data required:

.. literalinclude:: ../../analyses/european_windstorms/xmas_eve_1811/get_data.py

Script to make an individual frame - takes year, month, day, and hour as command-line options:

.. literalinclude:: ../../analyses/european_windstorms/xmas_eve_1811/video/x11_V3only.py

To make the video, it is necessary to run the script above hundreds of times - giving an image for every 15-minute period. This script makes the list of commands needed to make all the images, which can be run with `GNU parallel <https://www.gnu.org/software/parallel/>`_ or a system-specific faster method.

.. literalinclude:: ../../analyses/european_windstorms/xmas_eve_1811/video/make_frames.py

To turn the thousands of images into a movie, use `ffmpeg <http://www.ffmpeg.org>`_

.. code-block:: shell

    ffmpeg -r 24 -pattern_type glob -i xmas_1811/\*.png \
           -c:v libx264 -threads 16 -preset slow -tune animation \
           -profile:v high -level 4.2 -pix_fmt yuv420p -crf 25 \
           -c:a copy xmas_1811.mp4
