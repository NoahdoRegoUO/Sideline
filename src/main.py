import asyncio
import json

from services import editing_service, nba_stats_service, nba_clip_service
from services.endpoints import *
from services.constants import *
from classes.game import Game

# Global Variables
game_list = []
game_IDs = []

# Fetch NBA data
yesterdays_nba_wins = nba_stats_service.getYesterdaysWins()
yesterdays_nba_games = nba_stats_service.getYesterdaysGames()

yesterdays_nba_games = yesterdays_nba_games.sort_values(
    by=["GAME_ID", "PTS"], ascending=[True, False]
)

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
    highlights = []
    for clip in all_clips:
        check_hype = [
            word for word in highlight_keywords if (word in clip["playDesc"].split())
        ]
        if bool(check_hype):
            highlights.append(clip)
    print(highlights)


asyncio.run(main())
