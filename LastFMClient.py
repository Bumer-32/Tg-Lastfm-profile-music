import requests


class LastFMClient:
    API_URL = "https://ws.audioscrobbler.com/2.0/"

    def __init__(self, api_key: str, username: str) -> None:
        self.api_key = api_key
        self.username = username

    async def get_now_playing(self) -> tuple[str, str] | tuple[None, None]:
        params = {
            "method": "user.getrecenttracks",
            "user": self.username,
            "api_key": self.api_key,
            "format": "json",
            "limit": 1
        }

        data = requests.get(self.API_URL, params=params).json()
        track = data["recenttracks"]["track"][0]

        is_now_playing = track.get("@attr", {}).get("nowplaying") == "true"

        if not is_now_playing:
            return None, None

        artist = track["artist"]["#text"]
        name = track["name"]

        return artist, name
