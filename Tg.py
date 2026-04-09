from pyrogram import Client
from pyrogram.raw import functions
from pyrogram.raw.types import InputDocument
from pyrogram.file_id import FileId

from Save import TrackInfo


class Tg:
    def __init__(self):
        self.app = None
        self.chat_id = None

    async def start(self, api_id: int, api_hash: str, chat_id: int) -> None:
        self.chat_id = chat_id
        self.app = Client("my_account", api_id=api_id, api_hash=api_hash)
        await self.app.start()

    async def upload_and_set(self, path: str) -> tuple[int, int, bytes]:
        msg = await self.app.send_audio(self.chat_id, path)
        dec = FileId.decode(msg.audio.file_id)
        id = InputDocument(id=dec.media_id, access_hash=dec.access_hash, file_reference=dec.file_reference)
        await self.app.invoke(functions.account.SaveMusic(id=id))
        return dec.media_id, dec.access_hash, dec.file_reference

    async def move(self, track: TrackInfo) -> None:
        id = InputDocument(id=track.media_id, access_hash=track.access_hash, file_reference=track.file_reference)
        await self.app.invoke(functions.account.SaveMusic(id=id))

