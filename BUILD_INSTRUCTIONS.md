# Инструкция по сборке Windows .exe

## Проблема
Сборка не завершается, потому что отсутствуют компоненты Visual Studio для компиляции Windows приложений.

## Решение

### 1. Установите компоненты Visual Studio

1. Откройте **Visual Studio Installer**
2. Нажмите **Изменить** на установленной версии Visual Studio
3. Выберите рабочую нагрузку **"Разработка классических приложений на C++"** (Desktop development with C++)
4. Убедитесь, что установлены:
   - ✅ **MSVC v142 - VS 2019 C++ x64/x86 build tools** (или новее)
   - ✅ **C++ CMake tools for Windows**
   - ✅ **Windows 10 SDK** (или Windows 11 SDK)
5. Нажмите **Изменить** и дождитесь установки

### 2. После установки компонентов

Запустите сборку:
```batch
build_windows.bat
```

Или вручную:
```batch
venv\Scripts\activate
flet build windows
```

### 3. Где найти .exe файл

После успешной сборки .exe файл будет находиться в:
```
build\flutter\windows\build\runner\Release\csv_json_generator.exe
```

## Альтернатива (без Visual Studio)

Если установка Visual Studio невозможна, можно использовать PyInstaller для создания простого .exe, но без нативного UI Flet:

```batch
pip install pyinstaller
pyinstaller --onefile --windowed --name "CSV_JSON_Generator" main.py
```

Но это создаст приложение без Flet UI (будет использоваться веб-интерфейс).

