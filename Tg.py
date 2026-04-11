from pyrogram import Client
from pyrogram.file_id import FileId
from pyrogram.raw import functions
from pyrogram.raw.types import InputDocument


class Tg:
    def __init__(self):
        self.app = None
        self.chat_id = None

    async def start(self, api_id: int, api_hash: str, chat_id: int) -> None:
        self.chat_id = chat_id
        self.app = Client("my_account", api_id=api_id, api_hash=api_hash)
        await self.app.start()

    async def upload_and_set(self, path: str) -> int:
        msg = await self.app.send_audio(self.chat_id, path)
        dec = FileId.decode(msg.audio.file_id)
        id = InputDocument(id=dec.media_id, access_hash=dec.access_hash, file_reference=dec.file_reference)
        await self.app.invoke(functions.account.SaveMusic(id=id))
        return msg.audio.file_id

    async def move(self, file_id: int) -> None:
        dec = FileId.decode(file_id)
        id = InputDocument(id=dec.media_id, access_hash=dec.access_hash, file_reference=dec.file_reference)
        await self.app.invoke(functions.account.SaveMusic(id=id))

