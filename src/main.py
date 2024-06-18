import os
import asyncio
import json
import urllib.request
import random
import fastf1
import pandas as pd

from services import editing_service, nba_stats_service, nba_clip_service, f1_service
from endpoints import *
from constants import *
from classes.game import Game
from classes.highlight import Highlight
from pathlib import Path
from moviepy.editor import *


# Global Variables
game_list = []
game_IDs = []
path = Path(os.path.dirname(__file__))


def create_NBA_dunk_compilation():
    game_footage = []
    highlights = []

    print("Starting Program...")

    # Fetch NBA data
    print("Fetching NBA Data")
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

    # Define function for retrieving NBA clips
    async def main():
        all_clips = await get_nba_clips(game_IDs)
        for clip in all_clips:
            check_hype = [
                word for word in dunk_keywords if (word in clip["playDesc"].split())
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
    final_footage = editing_service.add_outro(final_footage)
    final_footage = editing_service.add_background_music(
        final_footage, "ceefour/" + get_background_music()
    )
    final_footage = editing_service.add_intro(final_footage)
    final_footage.write_videofile(str(path) + "/content/clips/nba-dunks-highlights.mp4")


def create_NBA_scorelines():
    scorelines = []

    print("Starting Program...")

    # Fetch NBA data
    print("Fetching NBA Data")
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

    for game in game_list:
        score_clip = editing_service.add_final_score_graphic(game, "nba")
        scorelines.append(score_clip)

    final_footage = concatenate_videoclips(scorelines)
    final_footage = editing_service.add_background_music(
        final_footage, "ceefour/" + get_background_music()
    )
    final_footage.write_videofile(str(path) + "/content/clips/nba-scores.mp4")


def create_NBA_highlights():
    game_footage = []
    highlights = []

    print("Starting Program...")

    # Fetch NBA data
    print("Fetching NBA Data")
    yesterdays_nba_games = nba_stats_service.getYesterdaysGames()

    yesterdays_nba_games = yesterdays_nba_games.sort_values(
        by=["GAME_ID", "PTS"], ascending=[True, False]
    )

    print("Creating Game Objects")

    for team in range(0, len(yesterdays_nba_games.index), 2):
        if team == len(yesterdays_nba_games.index) - 1:
            continue
        team_stats_1 = yesterdays_nba_games.iloc[team]
        team_stats_2 = yesterdays_nba_games.iloc[team + 1]
        game_obj = Game(team_stats_1, team_stats_2)
        if 40000000 < game_obj.id < 1000000000:
            print(game_obj)
            game_list.append(game_obj)
            game_IDs.append(game_obj.id)

    # Define function for retrieving NBA clips
    async def main(game_list):
        for game in game_list:
            game_highlights = []
            all_clips = await get_nba_clips([game.id])

            # Condition if no games are found
            if len(all_clips) == 0:
                print("No games found")
                exit()

            for clip in all_clips:
                check_hype = [
                    word
                    for word in highlight_keywords
                    if (word in clip["playDesc"].split())
                ]
                if bool(check_hype):
                    game_highlights.append(clip)

            # Save last clip (in case buzzer beater)
            last_clip = all_clips[-1]

            # Add 5 random clips
            for i in range(5):
                clip_num = random.randint(
                    min(i * 6, len(game_highlights) - 3),
                    min(i * 6 + 5, len(game_highlights) - 2),
                )
                highlights.append(game_highlights[clip_num])
                game_highlights.pop(clip_num)

            # Add last clip
            highlights.append(last_clip)

    print("Fetching NBA Clips...")

    asyncio.run(main(game_list))

    print("Creating video clips:")

    for clip in highlights:
        print(clip)
        game = None
        for item in game_list:
            if item is None:
                game_list.remove(item)
            elif isinstance(clip, CompositeVideoClip):
                continue
            elif item.id == clip["gameId"]:
                game = item
                break
        if game is not None:
            highlight = Highlight(game.id, clip["videoUrl"], clip["playDesc"])
            highlight.set_video_clip()
            game.add_highlight(highlight)

    print("Combining Clips...")

    for game in game_list:
        game.combine_highlights()
        if game.footage is not None:
            score_clip = editing_service.add_final_score_graphic(game, "nba")
            game_footage.append(score_clip)
            game.add_video_effects()
            game_footage.append(game.footage)

    print(game_footage)

    final_footage = concatenate_videoclips(game_footage)
    music = get_background_music()
    final_footage = editing_service.addMusicAttributionHeader(music, final_footage)
    final_footage = editing_service.add_outro(final_footage)
    final_footage = editing_service.add_background_music(
        final_footage, "ceefour/" + music
    )
    # final_footage = editing_service.add_intro(final_footage)
    final_footage.write_videofile(str(path) + "/content/clips/nba-highlights.mp4")


def create_WNBA_highlights():
    game_footage = []
    highlights = []

    print("Starting Program...")

    # Fetch NBA data
    print("Fetching WNBA Data")
    yesterdays_nba_games = nba_stats_service.getYesterdaysGames()

    yesterdays_nba_games = yesterdays_nba_games.sort_values(
        by=["GAME_ID", "PTS"], ascending=[True, False]
    )

    print("Creating Game Objects")

    for team in range(0, len(yesterdays_nba_games.index), 2):
        if team == len(yesterdays_nba_games.index) - 1:
            continue
        team_stats_1 = yesterdays_nba_games.iloc[team]
        team_stats_2 = yesterdays_nba_games.iloc[team + 1]
        game_obj = Game(team_stats_1, team_stats_2)
        if game_obj.id > 1020000000:
            print(game_obj)
            game_list.append(game_obj)
            game_IDs.append(game_obj.id)

    # Define function for retrieving NBA clips
    async def main(game_list):
        for game in game_list:
            game_highlights = []
            all_clips = await get_wnba_clips([game.id])
            for clip in all_clips:
                check_hype = [
                    word
                    for word in highlight_keywords
                    if (word in clip["playDesc"].split())
                ]
                if bool(check_hype):
                    game_highlights.append(clip)

            # Save last clip (in case buzzer beater)
            last_clip = all_clips[-1]

            # Add 5 random clips
            for i in range(5):
                clip_num = random.randint(
                    min(i * 6, len(game_highlights) - 3),
                    min(i * 6 + 5, len(game_highlights) - 2),
                )
                highlights.append(game_highlights[clip_num])
                game_highlights.pop(clip_num)

            # Add last clip
            highlights.append(last_clip)

    print("Fetching WNBA Clips...")

    asyncio.run(main(game_list))

    print("Creating video clips:")

    for clip in highlights:
        print(clip)
        game = None
        for item in game_list:
            if item is None:
                game_list.remove(item)
            elif isinstance(clip, CompositeVideoClip):
                continue
            elif item.id == clip["gameId"]:
                game = item
                break
        if game is not None:
            highlight = Highlight(game.id, clip["videoUrl"], clip["playDesc"])
            highlight.set_video_clip()
            game.add_highlight(highlight)

    print("Combining Clips...")

    for game in game_list:
        game.combine_highlights()
        if game.footage is not None:
            score_clip = editing_service.add_final_score_graphic(game, "wnba")
            game_footage.append(score_clip)
            game.add_video_effects()
            game_footage.append(game.footage)

    print(game_footage)

    final_footage = concatenate_videoclips(game_footage)
    music = get_background_music()
    final_footage = editing_service.addMusicAttributionHeader(music, final_footage)
    final_footage = editing_service.add_outro(final_footage)
    final_footage = editing_service.add_background_music(
        final_footage, "ceefour/" + music
    )
    # final_footage = editing_service.add_intro(final_footage)
    final_footage.write_videofile(str(path) + "/content/clips/wnba-highlights.mp4")


### F1 RESULTS ###
def create_f1_results_video():
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
        video = editing_service.add_outro(video)
        audioclip = AudioFileClip(
            str(path) + "/content/audio/ceefour" + get_background_music()
        ).subclip(0, video.duration)
        video = video.set_audio(audioclip)
        video = editing_service.add_intro(video)
        video.write_videofile(str(path) + "/content/clips/f1_results.mp4")


def get_background_music(index=None):
    song_names = os.listdir(str(path) + "/content/audio/ceefour")

    if index != None:
        return song_names[index]
    else:
        return song_names[random.randint(0, len(song_names) - 1)]


### VIDEOS TO CREATE ###
# create_NBA_dunk_compilation()
# create_NBA_scorelines()
create_NBA_highlights()
# create_WNBA_highlights()
# create_f1_results_video()

### FUNCTION TESTING ###
# print(get_background_music())
