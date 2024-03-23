import os
import numpy as np

from services import editing_service, nba_stats_service, nba_clip_service, f1_service
from moviepy.editor import *
from pathlib import Path

path = Path(os.path.dirname(__file__))

### F1 SERVICE TEST ###
race_info = f1_service.getYesterdaysRace()
race_results = None

if race_info is not None:
    round_number = race_info["RoundNumber"].item()
    race_results = f1_service.getYesterdaysResults(round_number)
else:
    print("No F1 Race Yesterday.")

### F1 RESULT TEST ###
tmp_vid = editing_service.addF1DriverResult(
    "1ST", "MAX VERSTAPPEN", "1:02:36", "+ 0:00"
)

tmp_vid.write_videofile(str(path) + "/content/clips/test_vid.mp4")

### INTRO - OUTRO TEST ###
# tmp_vid = VideoFileClip(str(path) + "/content/clips/tmp.mp4")
# tmp_vid = editing_service.add_intro(tmp_vid)
# tmp_vid = editing_service.add_outro(tmp_vid)

# test_vid = editing_service.add_outro(tmp_vid)

# test_vid.write_videofile(str(path) + "/content/clips/test_vid.mp4")
