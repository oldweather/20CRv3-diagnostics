Irish Gale of 1843 video
========================

.. raw:: html

    <center>
    <table><tr><td><center>
    <iframe src="https://player.vimeo.com/video/268017533?title=0&byline=0&portrait=0" width="795" height="448" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe></center></td></tr>
    <tr><td><center>MSLP Contours for v2c (left) and v3 (right)</center></td></tr>
    </table>
    </center>

The thin blue lines are mslp contours from each of 56 ensemble members (all members for v2c, the first 56 members for v3). The thicker black lines are contours of the ensemble mean. The yellow dots mark pressure observations assimilated while making the field shown.

|

The 1843 Irish Gale is described in `Stephen Burt's paper on Extreme British Isles depressions <https://rmets.onlinelibrary.wiley.com/doi/full/10.1002/wea.20>`_ and `Symons Magazine in 1892 (page 164) <https://digital.nmla.metoffice.gov.uk/download/file/sdb:digitalFile|62c9b162-7a06-4575-9b85-12989d6ef05a>`_.

Download the data required:

.. literalinclude:: ../../analyses/european_windstorms/Irish_Gale_1843/get_data.py

Script to make an individual frame - takes year, month, day, and hour as command-line options:

.. literalinclude:: ../../analyses/european_windstorms/Irish_Gale_1843/video/IG_V3vV2c.py

To make the video, it is necessary to run the script above hundreds of times - giving an image for every 15-minute period. The best way to do this is system dependent - the script below does it on the Met Office SPICE cluster - it will need modification to run on any other system. (Could do this on a single PC, but it will take many hours).

.. literalinclude:: ../../analyses/european_windstorms/Irish_Gale_1843/video/make_frames.py

To turn the thousands of images into a movie, use `ffmpeg <http://www.ffmpeg.org>`_

.. code-block:: shell

    ffmpeg -r 24 -pattern_type glob -i Irish_Gale_1843/\*.png \
           -c:v libx264 -threads 16 -preset slow -tune animation \
           -profile:v high -level 4.2 -pix_fmt yuv420p -crf 25 \
           -c:a copy Irish_Gale.mp4
