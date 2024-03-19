import os
import asyncio
import json
import urllib.request

from services import editing_service, nba_stats_service, nba_clip_service
from endpoints import *
from constants import *
from classes.game import Game
from classes.highlight import Highlight
from pathlib import Path
from moviepy.editor import *


# Global Variables
game_list = []
game_IDs = []
game_footage = []
highlights = []
path = Path(os.path.dirname(__file__))

print("Starting Program...")

# Fetch NBA data
print("Fetching NBA Data")
yesterdays_nba_wins = nba_stats_service.getYesterdaysWins()
yesterdays_nba_games = nba_stats_service.getYesterdaysGames()

yesterdays_nba_games = yesterdays_nba_games.sort_values(
    by=["GAME_ID", "PTS"], ascending=[True, False]
)

print("Creating Game Objects")

for team in range(0, len(yesterdays_nba_games.index), 2):
    team_stats_1 = yesterdays_nba_games.iloc[team]
    team_stats_2 = yesterdays_nba_games.iloc[team + 1]
    game_obj = Game(team_stats_1, team_stats_2)
    print(game_obj)
    game_list.append(game_obj)
    game_IDs.append(game_obj.id)

# for col in yesterdays_nba_games.columns:
#     print(col)


async def main():
    all_clips = await get_nba_clips(game_IDs)
    for clip in all_clips:
        check_hype = [
            word for word in highlight_keywords if (word in clip["playDesc"].split())
        ]
        if bool(check_hype):
            highlights.append(clip)
    print("Number of highlights: " + str(len(highlights)))


print("Fetching NBA Clips...")

asyncio.run(main())

print("Creating video clips:")

for clip in highlights:
    game = None
    for item in game_list:
        if item.id == clip["gameId"]:
            game = item
            break
    highlight = Highlight(game.id, clip["videoUrl"], clip["playDesc"])
    highlight.set_video_clip()
    game.add_highlight(highlight)

print("Combining Clips...")

for game in game_list:
    game.combine_highlights()
    if game.footage is not None:
        game.add_video_effects()
        game_footage.append(game.footage)

print(game_footage)

final_footage = concatenate_videoclips(game_footage)
final_footage = editing_service.add_intro(final_footage)
final_footage = editing_service.add_outro(final_footage)
final_footage.write_videofile(str(path) + "/content/clips/nba-dunks-highlights.mp4")
