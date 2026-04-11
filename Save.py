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
            return [TrackInfo(**t) for t in data]

    def save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump([asdict(t) for t in self.data], f, indent=2, ensure_ascii=False)

    def find(self, track: str) -> TrackInfo | None:
        return next((t for t in self.data if t.name == track), None)

    def add(self, track: TrackInfo) -> None:
        self.data.append(track)
        self.save()

@dataclass
class TrackInfo:
    name: str
    url: str
    file_id: int