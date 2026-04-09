import asyncio
import os
import subprocess


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