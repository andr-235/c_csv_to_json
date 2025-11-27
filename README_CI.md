# GitHub Actions CI/CD

Автоматическая сборка приложения для Windows и Linux через GitHub Actions.

## Как это работает

1. **При каждом push** в ветки `main` или `master` запускается автоматическая сборка
2. **При создании Release** автоматически создаются артефакты для скачивания
3. **Ручной запуск** через вкладку Actions в GitHub

## Workflow

### build.yml
Основной workflow для автоматической сборки:
- **Windows**: Собирает .exe файл через `flet build windows`
- **Linux**: Собирает .rpm пакет через `briefcase`
- Автоматически запускается при push, PR, создании Release или ручном запуске

## Где найти артефакты

### В GitHub Actions:

1. Перейдите в **Actions** на GitHub
2. Выберите последний успешный workflow run
3. Прокрутите вниз до секции **Artifacts**
4. Нажмите на артефакт для скачивания:
   - `windows-exe` - Windows исполняемый файл (.exe)
   - `linux-rpm` - Linux RPM пакет (.rpm)
   - `linux-deb` - Linux DEB пакет (.deb)

### Где находится exe после сборки:

После успешной сборки Windows exe файл находится в:
```
build/flutter/windows/build/runner/Release/csv_json_generator.exe
```

Или в корне проекта (скопирован для удобства):
```
csv_json_generator.exe
```

## Создание Release

1. Создайте новый **Release** на GitHub
2. Workflow автоматически соберет артефакты
3. Файлы будут прикреплены к Release

## Локальная сборка

Для локальной сборки используйте:
- Windows: `build_windows.bat`
- Linux: `./build_linux.sh`

## Требования для локальной сборки

- **Windows**: Visual Studio с компонентами C++ (см. BUILD_INSTRUCTIONS.md)
- **Linux**: `rpm-build`, `python3-dev`

