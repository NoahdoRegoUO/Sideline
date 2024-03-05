# Query nba.live.endpoints.scoreboard and  list games in localTimeZone
from datetime import date, datetime, timezone, timedelta
from dateutil import parser
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import leaguegamefinder

from . import constants

import pandas as pd


# Prints today's schedule
def getTodaysSchedule():
    f = "{gameId}: {awayTeam} vs. {homeTeam} @ {gameTimeLTZ}"

    board = scoreboard.ScoreBoard()
    print("Date: " + board.score_board_date)
    games = board.games.get_dict()
    for game in games:
        gameTimeLTZ = (
            parser.parse(game["gameTimeUTC"])
            .replace(tzinfo=timezone.utc)
            .astimezone(tz=None)
        )
        print(
            f.format(
                gameId=game["gameId"],
                awayTeam=game["awayTeam"]["teamName"],
                homeTeam=game["homeTeam"]["teamName"],
                gameTimeLTZ=gameTimeLTZ,
            )
        )


# Returns a table of yesterday's games
def getYesterdaysGames():
    yesterday = date.today() - timedelta(days=1)
    gamefinder = leaguegamefinder.LeagueGameFinder(
        date_from_nullable=yesterday.strftime("%m/%d/%Y"),
        date_to_nullable=yesterday.strftime("%m/%d/%Y"),
    )
    games = gamefinder.get_data_frames()[0]

    # Regex for checking teams
    team_list = "|".join(constants.nba_teams)

    # Pandas supports regex patterns
    nba_games = games[games.TEAM_ABBREVIATION.str.contains(team_list)]
    nba_games.head()
    return nba_games


# Returns a table of yesterday's won games
def getYesterdaysWins():
    all_games = getYesterdaysGames()
    games_won = all_games[all_games.WL.str.contains("W")]
    games_won.head()
    return games_won
