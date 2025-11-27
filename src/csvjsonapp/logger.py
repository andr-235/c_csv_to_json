import flet as ft
from .interfaces import ILogger


class TextFieldLogger(ILogger):
    def __init__(self, text_field: ft.TextField):
        self.text_field = text_field
    
    def log(self, message: str) -> None:
        self.text_field.value += f"\n{message}"
        self.text_field.update()

