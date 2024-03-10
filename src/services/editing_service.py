import os

from moviepy.editor import *
from pathlib import Path

# GLOBAL VARIABLES
path = Path(os.path.dirname(__file__))


def addSubtitle(title_text, clip):
    # Generate a text clip. You can customize the font, color, etc.
    txt_clip = TextClip(
        title_text,
        font="Avenir-Next-Condensed-Heavy",
        fontsize=36,
        color="white",
    )

    # Say that you want it to appear 10s at the center of the screen
    txt_clip = txt_clip.set_position(("left", "top")).set_duration(clip.duration)

    # Overlay the text clip on the first video clip
    video = CompositeVideoClip([clip, txt_clip])

    return video


def combine_videos(video1_path, video2_path, final_path):
    clip1 = VideoFileClip(video1_path)
    clip2 = VideoFileClip(video2_path)
    combined_clips = concatenate_videoclips([clip1, clip2], method="compose")
    combined_clips.write_videofile(final_path)


# clip = VideoFileClip(str(path.parent) + "/content/footage/Blazing_Fire.mp4").subclip(
#     20, 30
# )

# video = CompositeVideoClip([clip, addSubtitle("MAVS 108 - 102 - ATL", clip)])

# # Write the result to a file (many options available !)
# video.write_videofile(str(path.parent) + "/content/footage/new.mp4")
