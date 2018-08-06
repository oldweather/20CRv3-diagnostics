Sitka Hurricane (1880) video - spinup version
=============================================

.. seealso:: :doc:`Better version with added observations <Sitka_Hurricane_video>`

.. raw:: html

    <center>
    <table><tr><td><center>
    <iframe src="https://player.vimeo.com/video/282687764?title=0&byline=0&portrait=0" width="795" height="448" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe></center></td></tr>
    <tr><td><center>MSLP Contours for v2c (left) and v3 (right)</center></td></tr>
    </table>
    </center>

The thin blue lines are mslp contours from each of 56 ensemble members (all members for v2c, the first 56 members for v3). The thicker black lines are contours of the ensemble mean. The yellow dots mark pressure observations assimilated while making the field shown. 

20CRv3 reconstructed this event twice, one in the stream started in November 1879 (so October 1880 is still in the spinup period) - that's this version. The :doc:`version in the stream starting in November 1874 <Sitka_Hurricane_video>` is not only fully spun-up, but also includes more observations: the observations from the USS Jamestown (at Sitka) were added to those from the Jeannette (Arctic Ocean) and Yukon (North Pacific) in this version.

`The "Sitka Hurricane" <https://link.springer.com/chapter/10.1007/978-90-481-2828-0_7>`_ was an unusually strong storm that made landfall near Sitka, in Alaska, on October 26, 1880.

|

Download the data required:

.. literalinclude:: ../../analyses/north_american_severe_weather/sitka_hurricane_1880/get_data.py

Script to make an individual frame - takes year, month, day, and hour as command-line options:

.. literalinclude:: ../../analyses/north_american_severe_weather/sitka_hurricane_1880/video/SH_V3vV2c.py

To make the video, it is necessary to run the script above hundreds of times - giving an image for every 15-minute period. The best way to do this is system dependent - the script below does it on the Met Office SPICE cluster - it will need modification to run on any other system. (Could do this on a single PC, but it will take many hours).

.. literalinclude:: ../../analyses/north_american_severe_weather/sitka_hurricane_1880/video/make_frames.py

To turn the thousands of images into a movie, use `ffmpeg <http://www.ffmpeg.org>`_

.. code-block:: shell

    ffmpeg -r 24 -pattern_type glob -i Sitka_Hurricane/\*.png \
           -c:v libx264 -threads 16 -preset slow -tune animation \
           -profile:v high -level 4.2 -pix_fmt yuv420p -crf 25 \
           -c:a copy Sitks_Hurricane.mp4
