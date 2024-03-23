import fastf1
import pandas as pd
from datetime import datetime, date, timedelta


def getYesterdaysRace():
    # Get yesterday's date
    yesterday_date = date.today() - timedelta(days=1)

    # Fetch the schedule for the current season
    schedule = fastf1.get_event_schedule(date.today().year)

    print(schedule.columns)

    # Find the round closest to the current date
    yesterdays_race = None

    for index, row in schedule.iterrows():
        if pd.notnull(schedule["Session5Date"][index]):
            if (
                int(
                    (
                        schedule["Session5Date"][index].to_pydatetime().date()
                        - yesterday_date
                    ).days
                )
                == -16
            ):
                yesterdays_race = schedule.iloc[index]
    return yesterdays_race


def getYesterdaysResults(round_number):
    # Fetch the latest race data
    session = fastf1.get_session(year=2024, gp=round_number, identifier="Race")
    session.load(telemetry=False, weather=False, messages=False)

    return session
