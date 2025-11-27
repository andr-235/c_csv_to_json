# CSV to JSON Converter — Flet + Python

import flet as ft
import csv
import json
import os
import re
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Optional, Dict, List

DEFAULT_TEMPLATE = """{
    "id": "{id}",
    "name": "{name}",
    "email": "{email}",
    "photo_path": "{photo_path}"
}"""


class IPhotoFinder(ABC):
    @abstractmethod
    def find(self, photo_name: str, photos_folder: Path) -> str:
        pass


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


class ITemplateProcessor(ABC):
    @abstractmethod
    def process(self, template: str, data: Dict[str, str], photo_path: Optional[str] = None) -> str:
        pass


class TemplateProcessor(ITemplateProcessor):
    def process(self, template: str, data: Dict[str, str], photo_path: Optional[str] = None) -> str:
        filled_template = template
        
        for key, value in data.items():
            filled_template = filled_template.replace(f"{{{key}}}", str(value))
        
        if photo_path:
            filled_template = filled_template.replace("{photo_path}", photo_path)
        else:
            filled_template = self._remove_photo_path(filled_template)
        
        return filled_template
    
    def _remove_photo_path(self, template: str) -> str:
        template = re.sub(r',?\s*"photo_path"\s*:\s*"[^"]*"', '', template)
        template = re.sub(r',?\s*"photo_path"\s*:\s*null', '', template)
        template = re.sub(r',\s*}', '}', template)
        template = re.sub(r'{\s*,', '{', template)
        return template


class ILogger(ABC):
    @abstractmethod
    def log(self, message: str) -> None:
        pass


class TextFieldLogger(ILogger):
    def __init__(self, text_field: ft.TextField):
        self.text_field = text_field
    
    def log(self, message: str) -> None:
        self.text_field.value += f"\n{message}"
        self.text_field.update()


class CSVReader:
    def __init__(self, csv_path: str):
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV-файл не найден: {csv_path}")
        self.csv_path = csv_path
    
    def read(self) -> List[Dict[str, str]]:
        rows = []
        with open(self.csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        return rows


class JSONFileWriter:
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def write(self, filename: str, data: Dict) -> None:
        output_file = self.output_dir / filename
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


class JSONGenerator:
    def __init__(
        self,
        template_processor: ITemplateProcessor,
        photo_finder: IPhotoFinder,
        logger: ILogger
    ):
        self.template_processor = template_processor
        self.photo_finder = photo_finder
        self.logger = logger
    
    def generate(
        self,
        csv_path: str,
        photos_folder: Optional[str],
        template_str: str
    ) -> tuple[int, int]:
        try:
            csv_reader = CSVReader(csv_path)
            rows = csv_reader.read()
        except Exception as e:
            self.logger.log(f"Ошибка при чтении CSV: {e}")
            return 0, 1
        
        photos_path = Path(photos_folder) if photos_folder and os.path.exists(photos_folder) else None
        writer = JSONFileWriter()
        
        created_count = 0
        error_count = 0
        
        for row in rows:
            try:
                if "id" not in row:
                    self.logger.log("Ошибка: В CSV отсутствует колонка 'id'")
                    error_count += 1
                    continue
                
                photo_name = row.get("photo", "")
                found_photo = ""
                if photo_name and photos_path:
                    found_photo = self.photo_finder.find(photo_name, photos_path)
                
                processed_template = self.template_processor.process(
                    template_str,
                    row,
                    found_photo if found_photo else None
                )
                
                try:
                    result = json.loads(processed_template)
                except json.JSONDecodeError as e:
                    self.logger.log(f"Ошибка JSON для строки {row.get('id', 'unknown')}: {e}")
                    error_count += 1
                    continue
                
                writer.write(f"{row['id']}.json", result)
                created_count += 1
                
            except Exception as e:
                error_count += 1
                self.logger.log(f"Ошибка при обработке строки: {e}")
        
        return created_count, error_count


class AppUI:
    def __init__(self, page: ft.Page):
        self.page = page
        self.csv_file_path = ""
        self.photos_folder_path = ""
        self._setup_page()
        self._create_ui()
    
    def _setup_page(self) -> None:
        self.page.title = "CSV → JSON Generator"
        self.page.window.width = 800
        self.page.window.height = 700
    
    def _create_ui(self) -> None:
        self.log_field = ft.TextField(
            multiline=True,
            read_only=True,
            expand=True,
            value="Готов к работе\n"
        )
        
        self.template_field = ft.TextField(
            multiline=True,
            value=DEFAULT_TEMPLATE,
            expand=True,
            min_lines=10
        )
        
        self.file_picker = ft.FilePicker(on_result=self._on_csv_selected)
        self.folder_picker = ft.FilePicker(on_result=self._on_folder_selected)
        
        self.page.overlay.extend([self.file_picker, self.folder_picker])
        
        self.page.add(
            ft.Text("CSV → JSON Generator", size=24, weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.ElevatedButton(
                    "Выбрать CSV-файл",
                    on_click=lambda _: self.file_picker.pick_files(
                        allowed_extensions=["csv"],
                        dialog_title="Выберите CSV-файл"
                    )
                ),
                ft.ElevatedButton(
                    "Выбрать папку с фото",
                    on_click=lambda _: self.folder_picker.get_directory_path(
                        dialog_title="Выберите папку с фотографиями"
                    )
                ),
                ft.ElevatedButton("Сгенерировать JSON", on_click=self._on_generate)
            ]),
            ft.Text("JSON-шаблон:", weight=ft.FontWeight.BOLD),
            self.template_field,
            ft.Text("Логи:", weight=ft.FontWeight.BOLD),
            self.log_field
        )
    
    def _on_csv_selected(self, e: ft.FilePickerResultEvent) -> None:
        if e.files and len(e.files) > 0:
            self.csv_file_path = e.files[0].path
            self.log_field.value += f"Выбран файл: {e.files[0].name}\n"
            self.log_field.update()
    
    def _on_folder_selected(self, e: ft.FilePickerResultEvent) -> None:
        if e.path:
            self.photos_folder_path = e.path
            self.log_field.value += f"Папка фото: {e.path}\n"
            self.log_field.update()
    
    def _on_generate(self, e) -> None:
        if not self.csv_file_path:
            self.log_field.value += "\nОшибка: Выберите CSV-файл"
            self.log_field.update()
            return
        
        self.log_field.value += "\nНачало генерации..."
        self.log_field.update()
        
        app = App(self.log_field)
        created, errors = app.generate(
            self.csv_file_path,
            self.photos_folder_path if self.photos_folder_path else None,
            self.template_field.value
        )
        
        self.log_field.value += f"\n\nСоздано файлов: {created}"
        if errors > 0:
            self.log_field.value += f"\nОшибок: {errors}"
        self.log_field.update()


class App:
    def __init__(self, logger: ILogger):
        self.photo_finder = PhotoFinder()
        self.template_processor = TemplateProcessor()
        self.logger = logger
        self.generator = JSONGenerator(
            self.template_processor,
            self.photo_finder,
            self.logger
        )
    
    def generate(
        self,
        csv_path: str,
        photos_folder: Optional[str],
        template_str: str
    ) -> tuple[int, int]:
        return self.generator.generate(csv_path, photos_folder, template_str)


def main(page: ft.Page):
    ui = AppUI(page)


if __name__ == "__main__":
    ft.app(target=main)
