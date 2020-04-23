Just the fog 1850-2015
======================

.. raw:: html

    <center>
    <table><tr><td><center>
    <iframe src="https://player.vimeo.com/video/410963689?title=0&byline=0&portrait=0" width="795" height="448" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe></center></td></tr>
    <tr><td><center>Observations and uncertainty in 20CRv3</center></td></tr>
    </table>
    </center>

A weather field (near-surface temperature, wind and precipitation) from 20CRv3. Overlain with black dots marking regions with observations assimilated (of surface pressure), and the grey fog masks regions where the reanalysis is very uncertain (where the ensemble spread in sea-level pressure is not much smaller than the climatological variation).

The video shows the time variation of observation and fog coverage, over the years 1850-2015. The weather shown does not change (to show the weather changing the video would need to be **much** longer).
|

Code to make the figure
-----------------------

This video needs the full ensemble, for four variables, but only for one year (here 2014). You also need observations, and MSLP ensemble spreads for the full period (1850-2014).

Script to download the ensemble data:

.. literalinclude:: ../../analyses/fog/just_fog/fetch_data.py

Script to download the PRMSL ensemble spreads:

.. literalinclude:: ../../analyses/fog/just_fog/fetch_ensemble_spreads.py

Script to make an individual frame - takes year, month, day, and hour as command-line options:

.. literalinclude:: ../../analyses/fog/just_fog/20CRv3_released.py

That script uses a random noise field to generate the wind vectors, and we want every frame to use the same noise field, so make and store that.

.. literalinclude:: ../../analyses/fog/just_fog/make_z.py

The aim is to do the full period in 10 seconds (240 frames). That would be about 1 frame every 150 days, but just doing this does not work well - there is too much difference between consecutive frames. So instead I generate 1 frame every 2 years (about 80 frames) and then make two interpolation frames between each of those.

Script to make the 80 base frames:

.. literalinclude:: ../../analyses/fog/just_fog/make_frames.py

Scripts to add the interpolation frames.

.. literalinclude:: ../../analyses/fog/just_fog/make_dissolve_transition.py
.. literalinclude:: ../../analyses/fog/just_fog/make_dissolve_frames.py

To turn the hundreds of images into a movie, use `ffmpeg <http://www.ffmpeg.org>`_

.. code-block:: shell

    ffmpeg -r 24 -pattern_type glob -i 20CRv3_just_fog/\*.png \
           -c:v libx264 -threads 16 -preset slow -tune film \
           -profile:v high -level 4.2 -pix_fmt yuv420p \
           -b:v 5M -maxrate 5M -bufsize 20M \
           -c:a copy 20CRv3_just_fog.mp4
