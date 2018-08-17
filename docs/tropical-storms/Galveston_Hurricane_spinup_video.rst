Galveston Hurricane (1900) video (spinup comparison)
====================================================

.. raw:: html

    <center>
    <table><tr><td><center>
    <iframe src="https://player.vimeo.com/video/285500035?title=0&byline=0&portrait=0" width="795" height="448" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe></center></td></tr>
    <tr><td><center>MSLP Contours for the spinup stream (left) and the production stream (right)</center></td></tr>
    </table>
    </center>

The thin blue lines are mslp contours from each of 56 ensemble members (all members for v2c, the first 56 members for v3). The thicker black lines are contours of the ensemble mean. The yellow dots mark pressure observations assimilated while making the field shown. The red dots are the IBTRACS best-track observations for unnamed tropical storms - the southernmost is the `Galveston Hurricane <https://en.wikipedia.org/wiki/1900_Galveston_hurricane>`_.

|

Data for this period are available from two 20CRv3 streams. The production stream starting in September 1894, and a subsequent stream starting in September 1899, which is imperfectly spun-up by the date of the hurricane. This is a comparison of the two streams.

|


Script to make an individual frame - takes year, month, day, and hour as command-line options:

.. literalinclude:: ../../analyses/tropical-storms/Galveston_Hurricane_1900/spinup_version/video/Galveston_V3vV2c.py

To make the video, it is necessary to run the script above hundreds of times - giving an image for every 15-minute period. The best way to do this is system dependent - the script below does it on the Met Office SPICE cluster - it will need modification to run on any other system. (Could do this on a single PC, but it will take many hours).

.. literalinclude:: ../../analyses/tropical-storms/Galveston_Hurricane_1900/spinup_version/video/make_frames.py

To turn the thousands of images into a movie, use `ffmpeg <http://www.ffmpeg.org>`_

.. code-block:: shell

    ffmpeg -r 24 -pattern_type glob -i Galveston_Hurricane_sp/\*.png \
           -c:v libx264 -threads 16 -preset slow -tune animation \
           -profile:v high -level 4.2 -pix_fmt yuv420p -crf 25 \
           -c:a copy Galveston_Hurricane_sp.mp4
