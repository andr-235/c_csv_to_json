# CSV to JSON Converter — Flet + Python

import flet as ft
from typing import Optional
from .interfaces import ILogger
from .photo_finder import PhotoFinder
from .template_processor import TemplateProcessor
from .logger import TextFieldLogger
from .json_generator import JSONGenerator
from .template_loader import TemplateLoader


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
        
        try:
            default_template = TemplateLoader.load_default()
        except Exception as e:
            default_template = '{\n    "id": "{id}",\n    "name": "{name}",\n    "email": "{email}",\n    "photo_path": "{photo_path}"\n}'
            self.log_field.value += f"\nПредупреждение: не удалось загрузить шаблон по умолчанию: {e}\n"
        
        self.template_field = ft.TextField(
            multiline=True,
            value=default_template,
            expand=True,
            min_lines=10
        )
        
        self.file_picker = ft.FilePicker(on_result=self._on_csv_selected)
        self.folder_picker = ft.FilePicker(on_result=self._on_folder_selected)
        self.template_picker = ft.FilePicker(on_result=self._on_template_selected)
        
        self.page.overlay.extend([self.file_picker, self.folder_picker, self.template_picker])
        
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
            ft.Row([
                ft.ElevatedButton(
                    "Загрузить шаблон JSON",
                    on_click=lambda _: self.template_picker.pick_files(
                        allowed_extensions=["json"],
                        dialog_title="Выберите JSON-шаблон"
                    )
                ),
                ft.ElevatedButton(
                    "Сбросить шаблон",
                    on_click=self._on_reset_template
                )
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
    
    def _on_template_selected(self, e: ft.FilePickerResultEvent) -> None:
        if e.files and len(e.files) > 0:
            try:
                template_str = TemplateLoader.load_from_file(e.files[0].path)
                self.template_field.value = template_str
                self.template_field.update()
                self.log_field.value += f"Загружен шаблон: {e.files[0].name}\n"
                self.log_field.update()
            except Exception as ex:
                self.log_field.value += f"\nОшибка загрузки шаблона: {ex}\n"
                self.log_field.update()
    
    def _on_reset_template(self, e) -> None:
        default_template = TemplateLoader.load_default()
        self.template_field.value = default_template
        self.template_field.update()
        self.log_field.value += "\nШаблон сброшен к значениям по умолчанию\n"
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
    try:
        page.window.min_width = 800
        page.window.min_height = 600
        page.window.center()
        ui = AppUI(page)
    except Exception as e:
        import traceback
        error_msg = f"Ошибка при запуске приложения:\n{str(e)}\n\n{traceback.format_exc()}"
        
        try:
            import os
            log_dir = os.path.join(os.path.expanduser("~"), "csv_json_generator_logs")
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(log_dir, "error.log")
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"\n{'='*50}\n")
                f.write(f"UI Error: {error_msg}\n")
        except:
            pass
        
        try:
            page.add(
                ft.Text("Ошибка запуска", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.RED),
                ft.Text(error_msg, size=10, selectable=True, expand=True),
                ft.ElevatedButton("Закрыть", on_click=lambda _: page.window.close())
            )
            page.update()
        except Exception as ui_err:
            try:
                import os
                log_file = os.path.join(os.path.expanduser("~"), "csv_json_generator_logs", "error.log")
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(f"\nUI Error display failed: {ui_err}\n")
            except:
                pass
