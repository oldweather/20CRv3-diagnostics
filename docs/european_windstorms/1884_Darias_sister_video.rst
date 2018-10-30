:orphan:

Daria's sister storm of 1884 video
==================================

.. raw:: html

    <center>
    <table><tr><td><center>
    <iframe src="https://player.vimeo.com/video/267411399?title=0&byline=0&portrait=0" width="795" height="448" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe></center></td></tr>
    <tr><td><center>MSLP Contours for v2c (left) and v3 (right)</center></td></tr>
    </table>
    </center>

The thin blue lines are mslp contours from each of 56 ensemble members (all members for v2c, the first 56 members for v3). The thicker black lines are contours of the ensemble mean. The yellow dots mark pressure observations assimilated while making the field shown.

|

Storm :doc:`Daria in 1990 <1990_Daria_storm>` is an architype of a damaging European windstorm, but it might not be the worst we can expect. This storm in 1884 is called "Daria's big sister" as it might be a useful example of an even-more-severe storm, if we can reconstruct it well enough. This storm produced the lowest pressure reading ever recorded over the British Isles and continental Europe. In Ochtertyre, close to the town of Crieff in Scotland, the barometer dropped to 925.6 hPa (Marriott 1884).

Download the data required:

.. literalinclude:: ../../analyses/european_windstorms/Darias_sister_1884/get_data.py


Script to make an individual frame - takes year, month, day, and hour as command-line options:

.. literalinclude:: ../../analyses/european_windstorms/Darias_sister_1884/video/DS_V3vV2c.py

To make the video, it is necessary to run the script above hundreds of times - giving an image for every 15-minute period. The best way to do this is system dependent - the script below does it on the Met Office SPICE cluster - it will need modification to run on any other system. (Could do this on a single PC, but it will take many hours).

.. literalinclude:: ../../analyses/european_windstorms/Darias_sister_1884/video/make_frames.py

To turn the thousands of images into a movie, use `ffmpeg <http://www.ffmpeg.org>`_

.. code-block:: shell

    ffmpeg -r 24 -pattern_type glob -i Darias_sister/\*.png \
           -c:v libx264 -threads 16 -preset slow -tune animation \
           -profile:v high -level 4.2 -pix_fmt yuv420p -crf 25 \
           -c:a copy Darias_sister.mp4
