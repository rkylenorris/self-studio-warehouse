import orjson as oj

from zipfile import ZipFile
from base64 import b64decode
from pathlib import Path
from hashlib import sha256
from base_mind import BaseMindTracker, DataSourceType
from base64 import b64decode
from dataclasses import dataclass
from functools import lru_cache

from ..tracker_tools import get_hash, get_latest_file


@dataclass
class ZippedBackup:
    hash: str
    data: bytes


class DaylioTracker(BaseMindTracker):

    backup_name_pattern: str = 'backup*.daylio'
    last_backup_path: Path
    new_archive_hash: str
    new_json_hash: str

    def __init__(self, backup_path: Path, name: str = "Daylio") -> None:
        if not backup_path.exists:
            raise ValueError(f"{backup_path} must already exist.")
        super().__init__(name, backup_path, DataSourceType.FILE)
        self.ingested_file = self.ingested_path / "daylio.json"
        self.hash_archive_path: Path = self.hashes_path / "daylio_archive.txt"
        self.hash_json_path: Path = self.hashes_path / "daylio_json.txt"

    def get_data(self):
        most_recent_backup: Path = get_latest_file(self.data_source,
                                                   self.backup_name_pattern)

        if most_recent_backup != None and self._is_new(most_recent_backup):
            self.ingest_data()

    @lru_cache
    def _get_zipped_backup(self, path: Path) -> ZippedBackup:
        with ZipFile(path.absolute(), "r") as z:
            with z.open("backup.json") as f:
                data = b64decode(f.read())
                current_json_hash = get_hash(f.read())
        return ZippedBackup(hash=current_json_hash, data=data)

    def _write_new_hashes(self, archive_hash: str, json_hash: str):
        self._write_hash(archive_hash, self.hash_archive_path.name)
        self._write_hash(json_hash, self.hash_json_path.name)

    def _is_new(self, backup_archive: Path) -> bool:
        if not self.hash_archive_path.exists() and not self.hash_json_path.exists():
            zipped_backup = self._get_zipped_backup(backup_archive)
            self._write_new_hashes(archive_hash=get_hash(
                backup_archive.read_bytes()), json_hash=zipped_backup.hash)
            self.data = zipped_backup.data
            return True
        elif self.hash_archive_path.exists():
            last_hash = self.hash_archive_path.read_text().strip()
            current_hash = get_hash(backup_archive.read_bytes())
            archive_hashes_match = current_hash == last_hash

            zipped_backup = self._get_zipped_backup(backup_archive)

            if archive_hashes_match and self.hash_json_path.exists():
                last_json_hash = self.hash_json_path.read_bytes()

                new_json = not (last_json_hash == zipped_backup.hash)
                if new_json:
                    self.data = zipped_backup.data
                    self._write_new_hashes(current_hash, zipped_backup.hash)
                return new_json
            else:
                self.data = zipped_backup.data
                self._write_new_hashes(current_hash, zipped_backup.hash)
                return True
        else:
            zipped_backup = self._get_zipped_backup(backup_archive)
            self.data = zipped_backup.data
            self._write_new_hashes(archive_hash=get_hash(
                backup_archive.read_bytes()), json_hash=zipped_backup.hash)
            return True

    def ingest_data(self) -> None:
        data_text = self.data.decode("utf-8")
        json = oj.loads(data_text)
        json_bytes = oj.dumps(json, option=oj.OPT_INDENT_2)
        with self.ingested_path.open(mode="wb", encoding="utf-8") as j:
            j.write(json_bytes)
