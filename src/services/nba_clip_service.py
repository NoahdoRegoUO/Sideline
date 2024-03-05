import requests
import json


def clip_endpoint(game_IDs):
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


# clip = VideoFileClip(os.path.dirname(__file__) + "/Blazing_Fire.mp4").subclip(20, 30)

# clip.write_videofile(os.path.dirname(__file__) + "/New_Fire.mp4")
