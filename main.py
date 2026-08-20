import asyncio
import os
from time import sleep, time

from LastFMClient import LastFMClient
from Save import Save, TrackInfo
from Tg import Tg
from YouTube import YouTube

minimum_listen_time = 30
check_period = 5

class Main:
    # noinspection PyTypeChecker
    def __init__(self) -> None:
        self.api_id = int(os.environ.get("TG_API_ID"))
        self.api_hash = str(os.environ.get("TG_API_HASH"))
        self.chat_id = int(os.environ.get("TG_CHAT_ID"))
        self.last_fm_api_key = str(os.environ.get("LAST_FM_API_KEY"))
        self.last_fm_username = str(os.environ.get("LAST_FM_USERNAME"))

        yt_dlp_exec = str(os.environ.get("YT_DLP_EXEC"))

        self.last_fm = LastFMClient(api_key=self.last_fm_api_key, username=self.last_fm_username)
        self.yt = YouTube(output_dir="au", yt_dlp_exec=yt_dlp_exec)
        self.cache = Save(path="save/sav.json")
        self.tg = Tg()

        self.last_played = ""
        self.played_time = -1
        self.actually_last_played = ""

    async def sync_to_profile(self, for_search: str, name: str, artist: str):
        found_in_save = self.cache.find(for_search)
                        
        if found_in_save:
            print("moving")
            await self.tg.move(found_in_save.msg_id)
        else:
            print("searching")
            found = await self.yt.search(for_search)
            if not found:
                print("Search failed, try to update yt-dlp and search again")
                await self.yt.update()
                found = self.cache.find(for_search)

            if not found:
                print("Not found")
            else:
                print(f"found {found}")

                path = await self.yt.download(found)
                if not path:
                    print("Downloading failed, try to update yt-dlp and download again")
                    await self.yt.update()
                    path = await self.yt.download(found)

                if not path:
                    print("Download failed")
                else:
                    new_path = self.yt.process_track(path, name, artist)
                    print(new_path)

                    msg_id = await self.tg.upload_and_set(new_path)

                    self.cache.add(TrackInfo(name=for_search, msg_id=msg_id))
                    print("saved")
                    os.remove(new_path)


    async def run(self):
        await self.tg.start(api_id=self.api_id, api_hash=self.api_hash, chat_id=self.chat_id)

        await self.yt.update()

        while True:
            sleep(check_period)
            print("check")
            try:
                artist, name = await self.last_fm.get_now_playing()
                for_search = f"{artist} - {name}"

                if not artist:
                    self.played_time = 0
                    continue
                if self.last_played == for_search: continue # this only for moments when track already set

                if self.actually_last_played != for_search: # for moments when track are not set and you skip track
                    self.played_time = 0
                    self.actually_last_played = for_search
                    continue

                if self.played_time == 0: self.played_time = time()
                if time() - self.played_time < minimum_listen_time: continue

                await self.sync_to_profile(for_search, name, artist) # and do all dirty work

                self.last_played = for_search
                self.played_time = 0
            except Exception as e:
                print(e)


if __name__ == "__main__":
    asyncio.run(Main().run())