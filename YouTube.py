import asyncio
import os
import subprocess
from pathlib import Path

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3


class YouTube:
    def __init__(self, output_dir) -> None:
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        subprocess.run(["yt-dlp", "-U"], capture_output=True, text=True)

    @staticmethod
    async def search(query) -> str | None:
        process = await asyncio.create_subprocess_exec(
            "yt-dlp",
            f"ytsearch1:{query} official audio",
            "--print", "webpage_url",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, _ = await process.communicate()
        url = stdout.decode().strip()

        return url if url else None

    async def download(self, url) -> str:
        process = await asyncio.create_subprocess_exec(
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "-o", f"{self.output_dir}/%(title)s.%(ext)s",
            "--print", "after_move:filepath",
            url,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, _ = await process.communicate()
        return stdout.decode().strip()

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