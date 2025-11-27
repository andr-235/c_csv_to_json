# CSV to JSON Converter — Flet + Python

import flet as ft
import csv
import json
import os
import re
from pathlib import Path

DEFAULT_TEMPLATE = """{
    "id": "{id}",
    "name": "{name}",
    "email": "{email}",
    "photo_path": "{photo_path}"
}"""


def find_photo(photo_name: str, photos_folder: Path) -> str:
    if not photo_name or not photos_folder.exists():
        return ""
    
    photo_name_lower = photo_name.lower()
    extensions = [".jpg", ".jpeg", ".png"]
    
    for ext in extensions:
        full_name = photo_name_lower + ext.lower()
        for file in photos_folder.iterdir():
            if file.name.lower() == full_name:
                return file.name
        if photo_name_lower.endswith(ext.lower()):
            for file in photos_folder.iterdir():
                if file.name.lower() == photo_name_lower:
                    return file.name
    
    return ""


def generate_json_files(csv_path: str, photos_folder: str, template_str: str, log_field: ft.TextField):
    if not os.path.exists(csv_path):
        log_field.value += "\nОшибка: CSV-файл не найден"
        log_field.update()
        return
    
    photos_path = Path(photos_folder) if photos_folder and os.path.exists(photos_folder) else None
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    created_count = 0
    error_count = 0
    
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                try:
                    filled_template = template_str
                    
                    for col_name, col_value in row.items():
                        filled_template = filled_template.replace(f"{{{col_name}}}", str(col_value))
                    
                    photo_name = row.get("photo", "")
                    found_photo = ""
                    if photo_name and photos_path:
                        found_photo = find_photo(photo_name, photos_path)
                    
                    if found_photo:
                        filled_template = filled_template.replace("{photo_path}", found_photo)
                    else:
                        filled_template = re.sub(r',?\s*"photo_path"\s*:\s*"[^"]*"', '', filled_template)
                        filled_template = re.sub(r',?\s*"photo_path"\s*:\s*null', '', filled_template)
                        filled_template = re.sub(r',\s*}', '}', filled_template)
                        filled_template = re.sub(r'{\s*,', '{', filled_template)
                    
                    try:
                        result = json.loads(filled_template)
                    except json.JSONDecodeError as e:
                        log_field.value += f"\nОшибка JSON для строки {row.get('id', 'unknown')}: {e}"
                        error_count += 1
                        continue
                    
                    if "id" not in row:
                        log_field.value += f"\nОшибка: В CSV отсутствует колонка 'id'"
                        log_field.update()
                        return
                    
                    output_file = output_dir / f"{row['id']}.json"
                    with open(output_file, "w", encoding="utf-8") as out_f:
                        json.dump(result, out_f, ensure_ascii=False, indent=2)
                    
                    created_count += 1
                    
                except Exception as e:
                    error_count += 1
                    log_field.value += f"\nОшибка при обработке строки: {e}"
        
        log_field.value += f"\n\nСоздано файлов: {created_count}"
        if error_count > 0:
            log_field.value += f"\nОшибок: {error_count}"
        log_field.update()
        
    except Exception as e:
        log_field.value += f"\nОшибка при чтении CSV: {e}"
        log_field.update()


def main(page: ft.Page):
    page.title = "CSV → JSON Generator"
    page.window.width = 800
    page.window.height = 700
    
    csv_file_path = ""
    photos_folder_path = ""
    
    log_field = ft.TextField(
        multiline=True,
        read_only=True,
        expand=True,
        value="Готов к работе\n"
    )
    
    template_field = ft.TextField(
        multiline=True,
        value=DEFAULT_TEMPLATE,
        expand=True,
        min_lines=10
    )
    
    def on_csv_selected(e: ft.FilePickerResultEvent):
        nonlocal csv_file_path
        if e.files and len(e.files) > 0:
            csv_file_path = e.files[0].path
            log_field.value += f"Выбран файл: {e.files[0].name}\n"
            log_field.update()
    
    def on_folder_selected(e: ft.FilePickerResultEvent):
        nonlocal photos_folder_path
        if e.path:
            photos_folder_path = e.path
            log_field.value += f"Папка фото: {e.path}\n"
            log_field.update()
    
    def on_generate(e):
        if not csv_file_path:
            log_field.value += "\nОшибка: Выберите CSV-файл"
            log_field.update()
            return
        
        log_field.value += "\nНачало генерации..."
        log_field.update()
        
        generate_json_files(
            csv_file_path,
            photos_folder_path if photos_folder_path else "",
            template_field.value,
            log_field
        )
    
    file_picker = ft.FilePicker(on_result=on_csv_selected)
    folder_picker = ft.FilePicker(on_result=on_folder_selected)
    
    page.overlay.extend([file_picker, folder_picker])
    
    page.add(
        ft.Text("CSV → JSON Generator", size=24, weight=ft.FontWeight.BOLD),
        ft.Row([
            ft.ElevatedButton(
                "Выбрать CSV-файл",
                on_click=lambda _: file_picker.pick_files(
                    allowed_extensions=["csv"],
                    dialog_title="Выберите CSV-файл"
                )
            ),
            ft.ElevatedButton(
                "Выбрать папку с фото",
                on_click=lambda _: folder_picker.get_directory_path(
                    dialog_title="Выберите папку с фотографиями"
                )
            ),
            ft.ElevatedButton("Сгенерировать JSON", on_click=on_generate)
        ]),
        ft.Text("JSON-шаблон:", weight=ft.FontWeight.BOLD),
        template_field,
        ft.Text("Логи:", weight=ft.FontWeight.BOLD),
        log_field
    )


if __name__ == "__main__":
    ft.app(target=main)

