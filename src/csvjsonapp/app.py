# CSV to JSON Converter — Flet + Python

import flet as ft
from typing import Optional
from csvjsonapp.interfaces import ILogger
from csvjsonapp.photo_finder import PhotoFinder
from csvjsonapp.template_processor import TemplateProcessor
from csvjsonapp.logger import TextFieldLogger
from csvjsonapp.json_generator import JSONGenerator

DEFAULT_TEMPLATE = """{
    "id": "{id}",
    "name": "{name}",
    "email": "{email}",
    "photo_path": "{photo_path}"
}"""


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
        
        app = App(TextFieldLogger(self.log_field))
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
