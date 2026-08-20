import asyncio
import os
from pathlib import Path

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3


class YouTube:
    def __init__(self, output_dir, yt_dlp_exec) -> None:
        self.output_dir = output_dir
        self.yt_dlp_exec = yt_dlp_exec

        os.makedirs(output_dir, exist_ok=True)

    async def search(self, query) -> str | None:
        process = await asyncio.create_subprocess_exec(
            self.yt_dlp_exec,
            f"ytsearch1:{query} official audio",
            "--print", "webpage_url",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()
        url = stdout.decode().strip()
    
        if stderr:
            print(stderr)
            return None
        else:
            return url

    async def download(self, url) -> str | None:
        process = await asyncio.create_subprocess_exec(
            self.yt_dlp_exec,
            "-x",
            "--audio-format", "mp3",
            "-o", f"{self.output_dir}/%(title)s.%(ext)s",
            "--print", "after_move:filepath",
            url,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()
        path = stdout.decode().strip()
        if stderr:
            print(stderr)
            return None
        else:
            return path

    async def update(self) -> None:
        process = await asyncio.create_subprocess_exec(self.yt_dlp_exec, "-U")
        await process.wait()

    @staticmethod
    def process_track(path: str, track_name: str, artist: str) -> str:
        mp3 = MP3(path, ID3=EasyID3)

        mp3["artist"] = artist
        mp3["title"] = track_name
        mp3.save()

        file = Path(path)
        new_file = file.with_name(f"{track_name}.mp3")
        file.rename(new_file)

        return new_file