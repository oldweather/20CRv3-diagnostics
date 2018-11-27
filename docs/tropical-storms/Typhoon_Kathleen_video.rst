:orphan:

Typhoon Kathleen (1947) video
=============================

.. raw:: html

    <center>
    <table><tr><td><center>
    <iframe src="https://player.vimeo.com/video/303032820?title=0&byline=0&portrait=0" width="795" height="448" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe></center></td></tr>
    <tr><td><center>MSLP Contours for v2c (left) and v3 (right)</center></td></tr>
    </table>
    </center>

The thin blue lines are mslp contours from each of 56 ensemble members (all members for v2c, the first 56 members for v3). The thicker black lines are contours of the ensemble mean. The yellow dots mark pressure observations assimilated while making the field shown. The red dots mark cyclone observations (NCEP_type > 300 and < 500).

|

`Typhoon Kathleen <https://www.air-worldwide.com/Publications/AIR-Currents/2017/Typhoon-Kathleen--Devastating-Flooding-from-a-Dying-Storm/>`_ is still regarded as one of Japan’s costliest and most devastating precipitation-induced flood disasters. 

|

Code to make the figure
-----------------------

Download the data required:

.. literalinclude:: ../../analyses/tropical-storms/Typhoon_Kathleen_1947/get_data.py

Script to make an individual frame - takes year, month, day, and hour as command-line options:

.. literalinclude:: ../../analyses/tropical-storms/Typhoon_Kathleen_1947/Kathleen_V3vV2c.py

To make the video, it is necessary to run the script above hundreds of times - giving an image for every 15-minute period. This script makes the list of commands needed to make all the images, which can be run `in parallel <http://brohan.org/offline_assimilation/tools/parallel.html>`_.

.. literalinclude:: ../../analyses/tropical-storms/Typhoon_Kathleen_1947/video/make_frames.py

To turn the thousands of images into a movie, use `ffmpeg <http://www.ffmpeg.org>`_

.. code-block:: shell

    ffmpeg -r 24 -pattern_type glob -i Typhoon_Kathleen/\*.png \
           -c:v libx264 -threads 16 -preset slow -tune animation \
           -profile:v high -level 4.2 -pix_fmt yuv420p -crf 25 \
           -c:a copy Typhoon_Kathleen.mp4
