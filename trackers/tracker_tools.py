from pathlib import Path
from hashlib import sha256


def get_latest_file(dir_path: Path, name_pattern: str) -> Path:
    latest_backup: Path = max([f for f in dir_path.glob(
        name_pattern)], key=lambda x: x.stat().st_mtime)
    if not latest_backup or latest_backup == None:
        raise ValueError(
            f"Directory {dir_path} has no results matching pattern: '{name_pattern}'")

    return latest_backup


def get_hash(data: bytes) -> str:
    if type(data) == bytes:
        return sha256(data).hexdigest().strip()
    else:
        raise ValueError("Parameter 'data' must be of type bytes.")
