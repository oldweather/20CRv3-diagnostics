:orphan:

Okeechobee Hurricane (1928) video
=================================

.. raw:: html

    <center>
    <table><tr><td><center>
    <iframe src="https://player.vimeo.com/video/263353524?title=0&byline=0&portrait=0" width="795" height="448" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe></center></td></tr>
    <tr><td><center>MSLP Contours for v2c (left) and v3 (right)</center></td></tr>
    </table>
    </center>

The thin blue lines are mslp contours from each of 56 ensemble members (all members for v2c, the first 56 members for v3). The thicker black lines are contours of the ensemble mean. The yellow dots mark pressure observations assimilated while making the field shown. The red dots are the IBTRACS best-track observations for unnamed tropical storms - the southernmost is the `Okeechobee Hurricane <https://en.wikipedia.org/wiki/1928_Okeechobee_hurricane>`_.

As well as showing the storm, this video demonstrates an interesting difference between the uncertainties (ensemble spread) of the two versions: In v2c the ensemble narrows and broadens as the observations come and go, v3 does not show this effect.

|

Download the data required:

.. literalinclude:: ../../analyses/tropical-storms/Okeechobee_Hurricane_1928/get_data.py

Script to make an individual frame - takes year, month, day, and hour as command-line options:

.. literalinclude:: ../../analyses/tropical-storms/Okeechobee_Hurricane_1928/video/Okeechobee_V3vV2c.py

To make the video, it is necessary to run the script above hundreds of times - giving an image for every 15-minute period. The best way to do this is system dependent - the script below does it on the Met Office SPICE cluster - it will need modification to run on any other system. (Could do this on a single PC, but it will take many hours).

.. literalinclude:: ../../analyses/tropical-storms/Okeechobee_Hurricane_1928/video/make_frames.py

To turn the thousands of images into a movie, use `ffmpeg <http://www.ffmpeg.org>`_

.. code-block:: shell

    ffmpeg -r 24 -pattern_type glob -i Hurricane_Okeechobee/\*.png \
           -c:v libx264 -threads 16 -preset slow -tune animation \
           -profile:v high -level 4.2 -pix_fmt yuv420p -crf 25 \
           -c:a copy Hurricane_Okeechobee.mp4
