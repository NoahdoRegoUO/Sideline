import os
import numpy as np
import pandas as pd

from services import editing_service, nba_stats_service, nba_clip_service, f1_service
from moviepy.editor import *
from pathlib import Path
from datetime import datetime, date, timedelta

path = Path(os.path.dirname(__file__))

### F1 SERVICE TEST ###
race_info = f1_service.getYesterdaysRace()
race_results = None
f1_clips = []

if race_info is not None:
    round_number = race_info["RoundNumber"].item()
    race_results = f1_service.getYesterdaysResults(round_number)
else:
    print("No F1 Race Yesterday.")

if race_results:
    for index in range(0, len(race_results.results.index)):
        driver_info = race_results.results.iloc[index]

        # Set Custom Diff
        diff = ""
        if not any(
            substring in driver_info["Status"] for substring in ["Lap", "Finished"]
        ):
            diff = "DNF (" + driver_info["Status"] + ")"
        else:
            diff = driver_info["Status"]

        # Set Time
        time = ""
        if isinstance(driver_info["Time"], pd.Timedelta):
            time = str(driver_info["Time"])[7:-3]
            print(time[1])
            if int(time[1]) == 0:
                time = "+" + time
        else:
            time = ">1 Lap"

        # Add Result Clip
        f1_clips.append(
            editing_service.addF1DriverResult(
                str(driver_info["Position"]),
                driver_info["FullName"],
                driver_info["TeamName"],
                time,
                diff,
                driver_info["HeadshotUrl"],
            )
        )
        print(driver_info)

if len(f1_clips) > 0:
    video = concatenate_videoclips(f1_clips, method="compose")
    video.write_videofile(str(path) + "/content/clips/f1_results.mp4")

### F1 RESULT TEST ###
# tmp_vid = editing_service.addF1DriverResult(
#     "1ST", "MAX VERSTAPPEN", "1:02:36", "+ 0:00"
# )

# tmp_vid.write_videofile(str(path) + "/content/clips/test_vid.mp4")

### INTRO - OUTRO TEST ###
# tmp_vid = VideoFileClip(str(path) + "/content/clips/tmp.mp4")
# tmp_vid = editing_service.add_intro(tmp_vid)
# tmp_vid = editing_service.add_outro(tmp_vid)

# test_vid = editing_service.add_outro(tmp_vid)

# test_vid.write_videofile(str(path) + "/content/clips/test_vid.mp4")
