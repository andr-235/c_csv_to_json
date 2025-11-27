import json
import os
from pathlib import Path
from typing import Dict


class TemplateLoader:
    @staticmethod
    def load_default() -> str:
        template_path = Path(__file__).parent / "template.json"
        if template_path.exists():
            with open(template_path, "r", encoding="utf-8") as f:
                template_dict = json.load(f)
            return json.dumps(template_dict, ensure_ascii=False, indent=4)
        return '{\n    "id": "{id}",\n    "name": "{name}",\n    "email": "{email}",\n    "photo_path": "{photo_path}"\n}'
    
    @staticmethod
    def load_from_file(file_path: str) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл шаблона не найден: {file_path}")
        
        with open(file_path, "r", encoding="utf-8") as f:
            template_dict = json.load(f)
        
        return json.dumps(template_dict, ensure_ascii=False, indent=4)
    
    @staticmethod
    def save_to_file(template_str: str, file_path: str) -> None:
        try:
            template_dict = json.loads(template_str)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(template_dict, f, ensure_ascii=False, indent=4)
        except json.JSONDecodeError as e:
            raise ValueError(f"Неверный формат JSON: {e}")

