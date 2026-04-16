from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any
from enum import StrEnum, auto
# each top level source classes must inherit from this class and implement the methods and use naming convention "{source_name_title_case}Tracker"


class DataSourceType(StrEnum):
    FILE = auto()
    API = auto()
    DATABASE = auto()


class BaseTracker(ABC):

    name: str
    ingested_path: Path = Path("data/ingested")
    hashes_path: Path = Path("data/hashes")
    data: Any = None
    data_source: Any
    data_source_type: DataSourceType

    def __init__(self, name, data_source: Any, data_source_type: DataSourceType) -> None:
        super().__init__()
        self.name = name
        self.data_source = data_source
        self.ingested_path.mkdir(parents=True, exist_ok=True)
        self.hashes_path.mkdir(parents=True, exist_ok=True)

    def _write_hash(self, hash: str, name: str):
        hash_path = self.hashes_path / name
        hash_path.write_text(hash)

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def ingest_data(self) -> None:
        pass
