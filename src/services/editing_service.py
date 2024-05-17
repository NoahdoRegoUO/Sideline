import os
import urllib.request

from moviepy.editor import *
from pathlib import Path
from constants import *
from PIL import Image

# GLOBAL VARIABLES
path = Path(os.path.dirname(__file__))


def addScorelineHeader(title_text, clip):
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


def addF1DriverResult(position, name, team, time, diff, driver):
    # Generate Image clip for F1 background
    background = (
        ImageClip(str(path.parent) + "/content/images/f1-background.png")
        .set_duration(4)
        .set_position("center")
        .set_fps(60)
    )

    # Lambda function for converting number to ordinal
    ordinal = lambda n: "%d%s" % (
        n,
        "TSNRHTDD"[(n // 10 % 10 != 1) * (n % 10 < 4) * n % 10 :: 4],
    )

    # Add position in bottom right
    position_txt = (
        TextClip(
            ordinal(int(float(position))),
            font="Avenir-Next-Condensed-Heavy",
            fontsize=175,
            color="red",
        )
        .set_position((0.68, 0.6), relative=True)
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
        .set_position((0.1, 0.02), relative=True)
        .set_duration(background.duration)
    )

    # Add team name
    team_txt = (
        TextClip(
            team,
            font="Avenir-Next-Condensed-Heavy",
            fontsize=60,
            color="white",
        )
        .set_position((0.01, 0.21), relative=True)
        .set_duration(background.duration)
    )

    # Add time
    time_txt = (
        TextClip(
            time,
            font="Avenir-Next-Condensed-Heavy",
            fontsize=50,
            color="white",
        )
        .set_position((0.08, 0.41), relative=True)
        .set_duration(background.duration)
    )

    # Add time
    diff_txt = (
        TextClip(
            diff,
            font="Avenir-Next-Condensed-Heavy",
            fontsize=50,
            color="white",
        )
        .set_position((0.08, 0.6), relative=True)
        .set_duration(background.duration)
    )

    # Store driver image
    urllib.request.urlretrieve(
        driver, str(path.parent) + "/content/images/temp_f1_driver.png"
    )

    temp_img = Image.open(
        str(path.parent) + "/content/images/temp_f1_driver.png"
    ).convert("RGBA")

    edited_img = Image.new("RGBA", temp_img.size)
    edited_img.paste((225, 225, 225, 0), box=(0, 0) + temp_img.size)
    edited_img.paste(temp_img, mask=temp_img)
    edited_img.save(str(path.parent) + "/content/images/edited_f1_driver.png")

    driver_img = (
        ImageClip(str(path.parent) + "/content/images/edited_f1_driver.png")
        .set_duration(background.duration)
        .set_position((0.01, 0.01), relative=True)
    )

    # Overlay the text clip on the first video clip
    video = CompositeVideoClip(
        [background, position_txt, name_txt, team_txt, time_txt, diff_txt, driver_img]
    )

    return video


def add_final_score_graphic(game, league):
    background_graphic_clip = (
        ImageClip(str(path.parent) + "/content/images/sideline_score_template.png")
        .set_duration(3)
        .set_position("center")
        .set_fps(60)
    )
    background_graphic_clip = background_graphic_clip.resize(width=1280, height=720)

    # Add logo to top left
    logo_clip = (
        ImageClip(str(path.parent) + "/content/logos/leagues/" + league + ".png")
        .set_duration(background_graphic_clip.duration)
        .set_position((0.035, 0.03), relative=True)
    )

    logo_clip = logo_clip.resize(0.2)

    # Add nba image
    content_image = (
        ImageClip(str(path.parent) + "/content/images/tmp_nba_photo.jpg")
        .set_duration(background_graphic_clip.duration)
        .set_position((0.444, 0.173), relative=True)
    )

    content_image = content_image.resize(0.36)

    # Add team 1 text clip
    team_1_txt_clip = (
        TextClip(
            game.team_stats_1["TEAM_NAME"].upper(),
            font="Avenir-Next-Condensed-Heavy",
            fontsize=24,
            color="white",
            method="caption",
            align="center",
            size=(300, 20),
        )
        .set_position((0.148, 0.05), relative=True)
        .set_duration(background_graphic_clip.duration)
    )

    # Add team 1 logo
    team_1_logo_clip = (
        ImageClip(
            str(path.parent)
            + "/content/logos/"
            + league
            + "/"
            + game.team_stats_1["TEAM_ABBREVIATION"]
            + ".png"
        )
        .set_duration(background_graphic_clip.duration)
        .set_position((0.215, 0.09), relative=True)
    )

    team_1_logo_clip = team_1_logo_clip.resize(0.25)

    # Add team 1 score
    score_1_txt = (
        TextClip(
            str(game.team_stats_1["PTS"]),
            font="Avenir-Next-Condensed-Heavy",
            fontsize=100,
            color="white",
            stroke_color="white",
            stroke_width=4,
            kerning=-1,
            method="caption",
            align="center",
            size=(300, 200),
        )
        .set_position((0.145, 0.22), relative=True)
        .set_duration(background_graphic_clip.duration)
    )

    # Add team 2 text clip
    team_2_txt_clip = (
        TextClip(
            game.team_stats_2["TEAM_NAME"].upper(),
            font="Avenir-Next-Condensed-Heavy",
            fontsize=20,
            color="white",
            method="caption",
            align="center",
            size=(300, 20),
        )
        .set_position((0.148, 0.89), relative=True)
        .set_duration(background_graphic_clip.duration)
    )

    # Add team 2 logo
    team_2_logo_clip = (
        ImageClip(
            str(path.parent)
            + "/content/logos/"
            + league
            + "/"
            + game.team_stats_2["TEAM_ABBREVIATION"]
            + ".png"
        )
        .set_duration(background_graphic_clip.duration)
        .set_position((0.215, 0.70), relative=True)
    )

    team_2_logo_clip = team_2_logo_clip.resize(0.25)

    # Add team 2 score
    score_2_txt = (
        TextClip(
            str(game.team_stats_2["PTS"]),
            font="Avenir-Next-Condensed-Heavy",
            fontsize=100,
            color="white",
            stroke_color="white",
            stroke_width=4,
            kerning=-1,
            method="caption",
            align="center",
            size=(300, 200),
        )
        .set_position((0.145, 0.48), relative=True)
        .set_duration(background_graphic_clip.duration)
    )

    # Concatenate clips
    video = CompositeVideoClip(
        [
            background_graphic_clip,
            logo_clip,
            content_image,
            team_1_txt_clip,
            team_1_logo_clip,
            score_1_txt,
            team_2_txt_clip,
            team_2_logo_clip,
            score_2_txt,
        ]
    )

    return video


def combine_videos(video1_path, video2_path, final_path):
    clip1 = VideoFileClip(video1_path)
    clip2 = VideoFileClip(video2_path)
    combined_clips = concatenate_videoclips([clip1, clip2], method="compose")
    combined_clips.write_videofile(final_path)


def add_background_music(video, audio_file):
    music = AudioFileClip(str(path.parent) + "/content/audio/" + audio_file)
    audio = afx.audio_loop(music, duration=video.duration)
    audio = audio.fx(afx.volumex, 0.25)
    new_audioclip = (
        CompositeAudioClip([video.audio, audio]) if video.audio is not None else audio
    )
    video = video.set_audio(new_audioclip)
    return video


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
