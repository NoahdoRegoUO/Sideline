import os

from pathlib import Path


nba_teams = [
    "ATL",
    "BOS",
    "BKN",
    "CHA",
    "CHI",
    "CLE",
    "DAL",
    "DEN",
    "DET",
    "GSW",
    "HOU",
    "IND",
    "LAC",
    "LAL",
    "MEM",
    "MIA",
    "MIL",
    "MIN",
    "NOP",
    "NYK",
    "OKC",
    "ORL",
    "PHI",
    "PHX",
    "POR",
    "SAC",
    "SAS",
    "TOR",
    "UTA",
    "WAS",
]

highlight_keywords = ["dunk", "Dunk", "dunk,"]

intro_path = "/content/clips/sideline_intro.mp4"
outro_path = "/content/images/sideline_outro.png"

path = Path(os.path.dirname(__file__))
