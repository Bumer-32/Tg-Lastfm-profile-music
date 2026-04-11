import asyncio
import os
from time import sleep

from LastFMClient import LastFMClient
from Save import Save, TrackInfo
from Tg import Tg
from YouTube import YouTube


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
            artist, name = await self.last_fm.get_now_playing()
            for_search = f"{artist} - {name}"
            if not artist: continue
            if self.last_played == for_search: continue
            found_in_save = self.cache.find(for_search)
            if not found_in_save:
                print("searching")
                found = await self.yt.search(for_search)
                if found:
                    print(f"found {found}")
                    path = await self.yt.download(found)
                    print(path)
                    new_path = self.yt.process_track(path, name, artist)
                    print(new_path)
                    msg_id = await tg.upload_and_set(new_path)
                    self.cache.add(TrackInfo(name=for_search, url=found, msg_id=msg_id))
                    print("saved")
                    os.remove(new_path)
            else:
                print("moving")
                await tg.move(found_in_save.msg_id)
            self.last_played = for_search


if __name__ == "__main__":
    asyncio.run(Main().run())