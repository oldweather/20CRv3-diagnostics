Weather and fog in the Arctic in 1880 and 1881
==============================================

.. raw:: html

    <center>
    <table><tr><td><center>
    <iframe src="https://player.vimeo.com/video/365276568?title=0&byline=0&portrait=0" width="795" height="448" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe></center></td></tr>
    <tr><td><center>The effect of observations from USS Jeanette (central black dot) on the 20CRv3 reconstruction in the Arctic in 1880 and 1881.</center></td></tr>
    </table>
    </center>

Near-surface air temperature (2m - colours), 10m wind (vectors), and precipitation (green shading) from Version 3 of the Twentieth Century Reanalysis (first ensemble member). Black dots mark observations assimilated (of surface pressure), and the grey fog masks regions where the reanalysis is very uncertain (where the ensemble spread in sea-level pressure is not much smaller than the climatological variation).

This is a polar projection with the Arctic in the centre.

|

Code to make the figure
-----------------------

Script to make an individual frame - takes year, month, day, and hour as command-line options:

.. literalinclude:: ../../analyses/fog/1880_Arctic/arctic_fog.py

That script uses a random noise field to generate the wind vectors, and we want every frame to use the same noise field, so make and store that.

.. literalinclude:: ../../analyses/fog/1880_Arctic/make_z.py

To make the video, it is necessary to run the frame generation script above hundreds of times - giving an image for every hour. This script makes the list of commands needed to make all the images, which can be run `in parallel <http://brohan.org/offline_assimilation/tools/parallel.html>`_.

.. literalinclude:: ../../analyses/fog/1880_Arctic/make_frames.py

To turn the thousands of images into a movie, use `ffmpeg <http://www.ffmpeg.org>`_

.. code-block:: shell

    ffmpeg -r 24 -pattern_type glob -i 20CRv3_arctic_fog/\*.png \
           -c:v libx264 -threads 16 -preset veryslow -tune film \
           -profile:v high -level 4.2 -pix_fmt yuv420p \
           -b:v 5M -maxrate 5M -bufsize 20M \
           -c:a copy 20CRv3_arctic_fog.mp4
