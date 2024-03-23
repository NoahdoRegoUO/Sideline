import os

from moviepy.editor import *
from pathlib import Path
from constants import *

# GLOBAL VARIABLES
path = Path(os.path.dirname(__file__))


def addNBAScoreline(title_text, clip):
    # Generate a text clip at top left
    txt_clip = (
        TextClip(
            title_text,
            font="Avenir-Next-Condensed-Heavy",
            fontsize=40,
            color="white",
        )
        .set_position((0.08, 0.025), relative=True)
        .set_duration(clip.duration)
    )

    # Generate Image clip for text background at top left
    img_clip = (
        ImageClip(str(path.parent) + "/content/images/sideline_header.png")
        .set_duration(clip.duration)
        .set_position(("left", "top"))
    )

    img_clip = img_clip.resize(0.5)

    # Overlay the text clip on the first video clip
    video = CompositeVideoClip([clip, img_clip, txt_clip])

    return video


def addF1DriverResult(position, name, time, diff):
    # Generate Image clip for F1 background
    background = (
        ImageClip(str(path.parent) + "/content/images/f1-background.png")
        .set_duration(8)
        .set_position("center")
        .set_fps(60)
    )

    # Add position in top left
    position_txt = (
        TextClip(
            position,
            font="Avenir-Next-Condensed-Heavy",
            fontsize=100,
            color="white",
        )
        .set_position((0.01, 0.01), relative=True)
        .set_duration(background.duration)
    )

    # Add driver name
    name_txt = (
        TextClip(
            name,
            font="Avenir-Next-Condensed-Heavy",
            fontsize=60,
            color="white",
        )
        .set_position((0.01, 0.2), relative=True)
        .set_duration(background.duration)
    )

    # Add time
    time_txt = (
        TextClip(
            time,
            font="Avenir-Next-Condensed-Heavy",
            fontsize=60,
            color="white",
        )
        .set_position((0.08, 0.4), relative=True)
        .set_duration(background.duration)
    )

    # Add time
    diff_txt = (
        TextClip(
            diff,
            font="Avenir-Next-Condensed-Heavy",
            fontsize=60,
            color="white",
        )
        .set_position((0.08, 0.58), relative=True)
        .set_duration(background.duration)
    )

    # Overlay the text clip on the first video clip
    video = CompositeVideoClip([background, position_txt, name_txt, time_txt, diff_txt])

    return video


def combine_videos(video1_path, video2_path, final_path):
    clip1 = VideoFileClip(video1_path)
    clip2 = VideoFileClip(video2_path)
    combined_clips = concatenate_videoclips([clip1, clip2], method="compose")
    combined_clips.write_videofile(final_path)


def add_intro(video):
    intro_clip = VideoFileClip(str(path.parent) + intro_path)
    new_video = concatenate_videoclips([intro_clip, video], method="compose")
    return new_video


def add_outro(video):
    outro_clip = (
        ImageClip(str(path.parent) + outro_path).set_duration(10).set_position("center")
    )
    outro_clip = outro_clip.resize(width=1280, height=720)
    new_video = concatenate_videoclips([video, outro_clip], method="compose")
    return new_video
