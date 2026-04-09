import asyncio
import os
from time import sleep, time

from Save import Save, TrackInfo
from Tg import Tg
from YouTube import YouTube
from LastFMClient import LastFMClient


class Main:
    # noinspection PyTypeChecker
    def __init__(self) -> None:
        self.api_id = int(os.environ.get("TG_API_ID"))
        self.api_hash = str(os.environ.get("TG_API_HASH"))
        self.chat_id = int(os.environ.get("TG_CHAT_ID"))
        self.last_fm_api_key = str(os.environ.get("LAST_FM_API_KEY"))
        self.last_fm_username = str(os.environ.get("LAST_FM_USERNAME"))

        self.last_fm = LastFMClient(api_key=self.last_fm_api_key, username=self.last_fm_username)
        self.yt = YouTube(output_dir="au/")
        self.cache = Save(path="sav.json")
        self.last_played = ""


    async def run(self):
        tg = Tg()
        await tg.start(api_id=self.api_id, api_hash=self.api_hash, chat_id=self.chat_id)

        while True:
            sleep(5)
            print("check")
            now = await self.last_fm.get_now_playing()
            if not now: continue
            if self.last_played == now: continue
            found_in_save = self.cache.find(now)
            if not found_in_save:
                print("searching")
                found = await self.yt.search(now)
                if found:
                    print(f"found {found}")
                    path = await self.yt.download(found)
                    print(path)
                    media_id, access_hash, file_reference = await tg.upload_and_set(path)
                    self.cache.add(TrackInfo(name=now, url=found, media_id=media_id, access_hash=access_hash, file_reference=file_reference))
                    print("saved")
            else:
                print("moving")
                await tg.move(found_in_save)
            self.last_played = now


if __name__ == "__main__":
    asyncio.run(Main().run())