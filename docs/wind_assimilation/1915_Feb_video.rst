:orphan:

February 1915 with assimilated marine wind directions
=====================================================

.. raw:: html

    <center>
    <table><tr><td><center>
    <iframe src="https://player.vimeo.com/video/838336304?title=0&byline=0&portrait=0" width="795" height="448" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe></center></td></tr>
    <tr><td><center>MSLP Contours for v3 (left) and scout 5.7.6 (right)</center></td></tr>
    </table>
    </center>

A spaghetti-contour-plot of MSLP from the 80 ensemble members of each run. The dots mark pressure observations assimilated while making the field shown. The scout run also assimilated wind directions from some of the marine observations. Yellow highlighting marks areas where the spread in the pressure ensemble is less than in the other run - darker yellows show a larger reduction.

|

We observed, in the pressure-only assimilations, that assimilating isolated observations only constrained analysis pressures very close to the observation - effectively the observation constrained the pressure, but not the local meteorology, many different atmospheric states can produce the same pressure observations. Assimilating wind directions as well as pressures should constrain the meteorology as well as the pressure, allowing an isolated observation to have an effect on the pressure fields much further away from the observation location. This is essentially what we see in these results, the reductions in pressure spread are concentrated in areas close to, but not co-located with, isolated ships.

We chose this month as a test case because of the single ship in the Weddell Sea (`the Endurance, from the Imperial Trans-Antarctic Expedition <https://oldweather.github.io/Expeditions/voyages/Imperial_trans_antarctic.html>`_) which should show this effect clearly. And it does, assimilating the wind direction from that single ship (in addition to its pressure) produces a widespread and substantial reduction in regional analysis ensemble spread.


Download the data required:

.. literalinclude:: ../../analyses/wind_assimilation/Feb_1915/get_data.py

Script to make an individual frame - takes year, month, day, and hour as command-line options:

.. literalinclude:: ../../analyses/wind_assimilation/Feb_1915/video/V3v576.py

To make the video, it is necessary to run the script above hundreds of times - giving an image for every 15-minute period. This script makes the list of commands needed to make all the images, which can be run `in parallel <http://brohan.org/offline_assimilation/tools/parallel.html>`_.

.. literalinclude:: ../../analyses/wind_assimilation/Feb_1915/video/make_frames.py

To turn the thousands of images into a movie, use `ffmpeg <http://www.ffmpeg.org>`_

.. code-block:: shell

    ffmpeg -r 24 -pattern_type glob -i V3v576/\*.png \
           -c:v libx264 -threads 16 -preset slow -tune animation \
           -profile:v high -level 4.2 -pix_fmt yuv420p -crf 25 \
           -c:a copy V3v576.mp4
