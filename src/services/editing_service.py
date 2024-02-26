import os

from moviepy.editor import *
from pathlib import Path

# GLOBAL VARIABLES
path = Path(os.path.dirname(__file__))


def addTitle(title_text, clip):
    # Generate a text clip. You can customize the font, color, etc.
    txt_clip = TextClip(
        title_text,
        font="Avenir-Next-Condensed-Heavy",
        fontsize=70,
        color="white",
    )

    # Say that you want it to appear 10s at the center of the screen
    txt_clip = txt_clip.set_position(("center", "center")).set_duration(10)

    # Overlay the text clip on the first video clip
    video = CompositeVideoClip([clip, txt_clip])

    return video


clip = VideoFileClip(str(path.parent) + "/content/footage/Blazing_Fire.mp4").subclip(
    20, 30
)

video = CompositeVideoClip([clip, addTitle("TITLE", clip)])

# Write the result to a file (many options available !)
video.write_videofile(str(path.parent) + "/content/footage/new.mp4")
