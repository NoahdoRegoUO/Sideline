import os
import requests
import json
import urllib.request

from . import editing_service
from pathlib import Path


# Global Variables
path = Path(os.path.dirname(__file__))


def nba_clip_endpoint(game_IDs):
    url = "https://thehighlow.io/api/query?isNba=true&season=2023-24&ordsq=&gameId=0&period=0&gameClock=12:00&eventNum=0"

    payload = json.dumps(
        {"queryType": "gameId", "gameIds": game_IDs, "videoType": "high"}
    )
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Cookie": "_ga=GA1.1.604633475.1707932015; _ga_J90Z6MZNMP=GS1.1.1709419676.6.0.1709419676.0.0.0",
        "Origin": "https://thehighlow.io",
        "Referer": "https://thehighlow.io/video/games/nba/2023-24/22300860?videoType=high",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()


def wnba_clip_endpoint(game_IDs):
    url = "https://thehighlow.io/api/query?isNba=false&season=2023-24&ordsq=&gameId=0&period=0&gameClock=12:00&eventNum=0"

    payload = json.dumps(
        {"queryType": "gameId", "gameIds": game_IDs, "videoType": "high"}
    )
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Cookie": "_ga=GA1.1.604633475.1707932015; _ga_J90Z6MZNMP=GS1.1.1709419676.6.0.1709419676.0.0.0",
        "Origin": "https://thehighlow.io",
        "Referer": "https://thehighlow.io/video/games/nba/2023-24/22300860?videoType=high",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()


def combine_game_highlights(highlights):
    tmpCount = 1

    urllib.request.urlretrieve(
        highlights[0]["videoUrl"],
        str(path.parent) + "/content/clips/combined_clips" + str(tmpCount) + ".mp4",
    )

    highlights.pop(0)

    for clip in highlights:
        clip_path = (
            str(path.parent) + "/content/clips/highlight_" + str(tmpCount) + ".mp4"
        )
        urllib.request.urlretrieve(
            clip["videoUrl"],
            clip_path,
        )
        editing_service.combine_videos(
            str(path.parent)
            + "/content/clips/"
            + "combined_clips"
            + str(tmpCount)
            + ".mp4",
            clip_path,
            str(path.parent)
            + "/content/clips/combined_clips"
            + str(tmpCount + 1)
            + ".mp4",
        )
        os.remove(clip_path)
        os.remove(
            str(path.parent)
            + "/content/clips/"
            + "combined_clips"
            + str(tmpCount)
            + ".mp4"
        )
        tmpCount += 1

    os.rename(
        str(path.parent) + "/content/clips/combined_clips" + str(tmpCount) + ".mp4",
        str(path.parent) + "/content/clips/all_highlights.mp4",
    )
