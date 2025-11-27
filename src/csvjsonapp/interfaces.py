from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Optional


class IPhotoFinder(ABC):
    @abstractmethod
    def find(self, photo_name: str, photos_folder: Path) -> str:
        pass


class ITemplateProcessor(ABC):
    @abstractmethod
    def process(self, template: str, data: Dict[str, str], photo_path: Optional[str] = None) -> str:
        pass


class ILogger(ABC):
    @abstractmethod
    def log(self, message: str) -> None:
        pass

