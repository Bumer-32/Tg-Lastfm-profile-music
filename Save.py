import base64
import json
import os
from dataclasses import dataclass, asdict


class Save:
    def __init__(self, path: str) -> None:
        self.path = path
        self.data = self._load()

    def _load(self) -> list:
        if not os.path.exists(self.path):
            return []
        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [TrackInfo.from_dict(t) for t in data]

    def save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in self.data], f, indent=2, ensure_ascii=False)

    def find(self, track: str) -> TrackInfo | None:
        return next((t for t in self.data if t.name == track), None)

    def add(self, track: TrackInfo) -> None:
        self.data.append(track)
        self.save()

@dataclass
class TrackInfo:
    name: str
    url: str
    media_id: int
    access_hash: int
    file_reference: bytes

    def to_dict(self):
        return {
            "name": self.name,
            "url": self.url,
            "media_id": self.media_id,
            "access_hash": self.access_hash,
            "file_reference": base64.b64encode(self.file_reference).decode()
        }

    @staticmethod
    def from_dict(data):
        return TrackInfo(
            name=data["name"],
            url=data["url"],
            media_id=data["media_id"],
            access_hash=data["access_hash"],
            file_reference=base64.b64decode(data["file_reference"])
        )