from moviepy.editor import *

from services.editing_service import *


class Game:
    def __init__(self, team_stats_1, team_stats_2):
        self.team_stats_1 = team_stats_1
        self.team_stats_2 = team_stats_2
        self.id = int(team_stats_1["GAME_ID"])
        self.scoreline = (
            self.team_stats_1["TEAM_ABBREVIATION"]
            + " "
            + str(self.team_stats_1["PTS"])
            + " - "
            + str(self.team_stats_2["PTS"])
            + " "
            + self.team_stats_2["TEAM_ABBREVIATION"]
        )
        self.highlights = []
        self.footage = None

    def __str__(self):
        return f"{self.id}: {self.scoreline}"

    def add_highlight(self, clip):
        self.highlights.append(clip)

    def combine_highlights(self):
        if not self.highlights:
            print("No highlights from game (" + self.scoreline + ")")
        else:
            highlight_clips = []
            for clip in self.highlights:
                highlight_clips.append(clip._video_clip)
            print(highlight_clips)
            self.footage = concatenate_videoclips(highlight_clips)

    def add_video_effects(self):
        self.footage = addSubtitle(self.scoreline, self.footage)
