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


def flatten_json(json: object, exclude: list[str] | None = None, max_depth: int = 1, current_depth=0, path: str = "") -> dict:

    result = {}

    if current_depth == max_depth:
        result[path] = json
    elif json is dict:
        for key, val in json.items():
            new_path = f"{path}.{key}"
            result.update(flatten_json(val, max_depth=max_depth,
                          current_depth=current_depth+1, path=new_path))
    elif json is list:
        for i, val in enumerate(json):
            new_path = f"{path}.{i}"
            result.update(flatten_json(val, max_depth=max_depth,
                          current_depth=current_depth+1, path=new_path))
    else:
        result[path] = json

    return result
