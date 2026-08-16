import os
from Save import Save, TrackInfo
from pyrogram import Client

api_id = int(os.environ.get("TG_API_ID"))
api_hash = str(os.environ.get("TG_API_HASH"))
chat_id = int(os.environ.get("TG_CHAT_ID"))

def main():
    save = Save("save/sav.json")
    app = Client("save/my_account", api_id=api_id, api_hash=api_hash)
    with app:
        for message in app.get_chat_history(chat_id=chat_id):
            if message.audio:
                name = f"{message.audio.performer} - {message.audio.file_name.replace(".mp3", "")}"
                id = message.id
                print(name, id)
                save.add(TrackInfo(name, id))

if __name__ == "__main__":
    main()