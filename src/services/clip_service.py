import os

from moviepy.editor import *

clip = VideoFileClip(os.path.dirname(__file__) + "/Blazing_Fire.mp4").subclip(20, 30)

clip.write_videofile(os.path.dirname(__file__) + "/New_Fire.mp4")
