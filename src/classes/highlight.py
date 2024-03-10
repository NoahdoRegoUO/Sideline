import os
import urllib.request

from moviepy.editor import *
from pathlib import Path

path = Path(os.path.dirname(__file__))


class Highlight:
    def __init__(self, game_id, video_url, play_desc):
        self._game_id = game_id
        self._video_url = video_url
        self._play_desc = play_desc
        self._video_clip = None

    def __str__(self):
        return f"{self._play_desc}"

    def set_video_clip(self):
        clip_path = str(path.parent) + "/content/clips/highlight.mp4"
        urllib.request.urlretrieve(self._video_url, clip_path)
        self._video_clip = VideoFileClip(clip_path)
        os.remove(clip_path)
