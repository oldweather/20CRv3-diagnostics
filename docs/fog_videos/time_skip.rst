Weather and fog 1850-2015
=========================

.. raw:: html

    <center>
    <table><tr><td><center>
    <iframe src="https://player.vimeo.com/video/410322672?title=0&byline=0&portrait=0" width="795" height="448" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe></center></td></tr>
    <tr><td><center>Weather, observations, and uncertainty in 20CRv3</center></td></tr>
    </table>
    </center>

Near-surface air temperature (2m - colours), 10m wind (vectors), and precipitation (green shading) from Version 3 of the Twentieth Century Reanalysis (first ensemble member). Black dots mark observations assimilated (of surface pressure), and the grey fog masks regions where the reanalysis is very uncertain (where the ensemble spread in sea-level pressure is not much smaller than the climatological variation).

To show the full period at this speed would produce almost 17 hours of video, so this is a sample: after showing 10 days of weather, the video jumps forward in time about 10 years.

|

Code to make the figure
-----------------------

This video is expensive in its data requirements: you have to download the full ensemble, for four variables, for each year included. That's about 5Tb of data. You also need temperature normals, and MSLP ensemble spreads, but that's a much smaller quantity.

Script to download the ensemble data:

.. literalinclude:: ../../analyses/fog/time_skips/fetch_data.py

Script to download the PRMSL ensemble spreads:

.. literalinclude:: ../../analyses/fog/time_skips/fetch_ensemble_spreads.py

Script to make an individual frame - takes year, month, day, and hour as command-line options:

.. literalinclude:: ../../analyses/fog/time_skips/20CRv3_released.py

That script uses a random noise field to generate the wind vectors, and we want every frame to use the same noise field, so make and store that.

.. literalinclude:: ../../analyses/fog/time_skips/make_z.py

To make the video, it is necessary to run the frame generation script above hundreds of times - giving an image for every hour. This script makes the list of commands needed to make all the images, which can be run `in parallel <http://brohan.org/offline_assimilation/tools/parallel.html>`_.

.. literalinclude:: ../../analyses/fog/time_skips/make_frames.py

There is a discontinuity in the video at each of the time skips, which would be visually jarring. These two scripts smooth these discontinuities by adding a few interpolated frames between the end of one time period and the start of the next.

.. literalinclude:: ../../analyses/fog/time_skips/make_dissolve_transition.py
.. literalinclude:: ../../analyses/fog/time_skips/make_dissolve_frames.py

To turn the thousands of images into a movie, use `ffmpeg <http://www.ffmpeg.org>`_

.. code-block:: shell

    ffmpeg -r 24 -pattern_type glob -i 20CRv3_time_skips/\*.png \
           -c:v libx264 -threads 16 -preset slow -tune film \
           -profile:v high -level 4.2 -pix_fmt yuv420p \
           -b:v 5M -maxrate 5M -bufsize 20M \
           -c:a copy 20CRv3_time_skips.mp4
