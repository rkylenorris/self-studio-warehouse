import os
import orjson as oj

from zipfile import ZipFile
from base64 import b64decode
from pathlib import Path
from hashlib import sha256
from base_mind import BaseMindTracker


class DaylioTracker(BaseMindTracker):

    backup_name_pattern: str = 'backup*.daylio'
    last_backup_path: Path
    new_archive_hash: str
    new_json_hash: str

    def __init__(self, backup_path: Path) -> None:
        if not backup_path.exists:
            raise ValueError(f"{backup_path} must already exist.")
        super().__init__()
        self.hash_archive_path: Path = self.hashes_path / "daylio_archive.txt"
        self.hash_json_path: Path = self.hashes_path / "daylio_json.txt"
        self.data_source = backup_path

    def get_data(self):
        most_recent_backup = max([f for f in self.data_source.glob(self.backup_name_pattern)],
                                 key=lambda x: x.stat().st_mtime)

    def ingest_data(self) -> None:
        return super().ingest_data()

    def _get_hash(self, data: bytes) -> str:
        return sha256(data).hexdigest()

    def _get_archive_hash(self, data: bytes):
        self._get_hash(data)

    # def is_new(self, path: Path, is_archive: bool):
    #     if not self.hash_archive_path.exists():
    #         return True
    #     elif is_archive:
    #         current_hash = self.get_hash(path.read_bytes())
    #         if current_hash == self.hash_archive_path.read_text().strip():
    #             return True
    #     elif self.hash_json_path.exists():
    #         with ZipFile(path, "r") as z:
    #             with z.open("backup.json", "r") as f:
    #                 current_hash = self.get_hash(f.read())
    #                 if current_hash == self.hash_json_path.read_text().strip():
    #                     return True
    #     elif not self.hash_json_path.exists():
    #         return True
    #     else:
    #         return False
