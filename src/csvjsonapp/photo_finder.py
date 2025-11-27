from pathlib import Path
from typing import List
from .interfaces import IPhotoFinder


class PhotoFinder(IPhotoFinder):
    def __init__(self, extensions: List[str] = None):
        self.extensions = extensions or [".jpg", ".jpeg", ".png"]
    
    def find(self, photo_name: str, photos_folder: Path) -> str:
        if not photo_name or not photos_folder.exists():
            return ""
        
        photo_name_lower = photo_name.lower()
        
        for ext in self.extensions:
            full_name = photo_name_lower + ext.lower()
            for file in photos_folder.iterdir():
                if file.name.lower() == full_name:
                    return file.name
            if photo_name_lower.endswith(ext.lower()):
                for file in photos_folder.iterdir():
                    if file.name.lower() == photo_name_lower:
                        return file.name
        
        return ""

