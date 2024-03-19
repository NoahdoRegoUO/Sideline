import os

from services import editing_service, nba_stats_service, nba_clip_service, f1_service
from moviepy.editor import *
from pathlib import Path

path = Path(os.path.dirname(__file__))

### F1 SERVICE TEST ###
f1_service.getYesterdaysStandings()

### INTRO - OUTRO TEST ###
# tmp_vid = VideoFileClip(str(path) + "/content/clips/tmp.mp4")
# tmp_vid = editing_service.add_intro(tmp_vid)
# tmp_vid = editing_service.add_outro(tmp_vid)

# test_vid = editing_service.add_outro(tmp_vid)

# test_vid.write_videofile(str(path) + "/content/clips/test_vid.mp4")
