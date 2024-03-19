import fastf1
import pandas as pd
from datetime import datetime, date, timedelta


def getYesterdaysStandings():
    # Get yesterday's date
    yesterday_date = date.today() - timedelta(days=1)

    # Fetch the schedule for the current season
    schedule = fastf1.get_event_schedule(date.today().year)

    print(schedule.columns)

    # Find the round closest to the current date
    session_date = schedule["Session5Date"][1].to_pydatetime().date()
    print((session_date - date.today()).days)

    yesterdays_race = None

    for index, row in schedule.iterrows():
        if pd.notnull(schedule["Session5Date"][index]):
            if (
                int(
                    (
                        schedule["Session5Date"][index].to_pydatetime().date()
                        - date.today()
                    ).days
                )
                == 1
            ):
                yesterdays_race = schedule["Session5Date"][index]

    print(yesterdays_race)

    print(closest_round)

    # Get the round number
    latest_round = closest_round["round"]

    # Fetch the latest race data
    session = fastf1.get_session(
        season=2024, round=latest_round, include=["Drivers", "LapTimes"]
    )

    # Extract the standings
    standings = session.classification
    print("Standings from the latest race:")
    for position, driver in enumerate(standings, start=1):
        print(
            f"{position}. {driver['Driver']} - {driver['Time']} - {driver['Laps']} laps"
        )
