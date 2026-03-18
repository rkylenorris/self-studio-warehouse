from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any
# each top level source classes must inherit from this class and implement the methods and use naming convention "{source_name_title_case}Source"


class BaseTracker(ABC):

    ingested_path: Path = Path("data/ingested")
    hashes_path: Path = Path("data/hashes")
    data: Any = None

    def __init__(self) -> None:
        super().__init__()
        self.ingested_path.mkdir(parents=True, exist_ok=True)
        self.hashes_path.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def ingest_data(self) -> None:
        pass
