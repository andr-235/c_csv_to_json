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
   - `windows-exe` - Windows исполняемый файл (.exe) + все необходимые DLL
   - `linux-rpm` - Linux RPM пакет (.rpm)

### Где находится exe после сборки:

После успешной сборки Windows exe файл находится в:
```
build/flutter/windows/build/runner/Release/csv_json_generator.exe
```

Или в корне проекта (скопирован для удобства):
```
csv_json_generator.exe
```

## Автоматическое создание Release

### Способ 1: Push тега (рекомендуется)

1. Создайте и запушьте тег:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. Workflow автоматически:
   - Соберет все артефакты (Windows .exe + DLL, Linux .rpm)
   - Создаст Release с этим тегом
   - Прикрепит все файлы к Release
   - Сгенерирует release notes

### Способ 2: Ручное создание Release

1. Перейдите в раздел **Releases** на GitHub
2. Нажмите **"Create a new release"**
3. Укажите:
   - **Tag version**: например `v1.0.0`
   - **Release title**: например `Version 1.0.0`
   - **Description**: описание изменений (опционально)
4. Нажмите **"Publish release"**
5. Workflow автоматически прикрепит артефакты к существующему Release

**Важно:** После создания Release все файлы будут доступны для скачивания прямо на странице Release.

## Локальная сборка

Для локальной сборки используйте:
- Windows: `build_windows.bat`
- Linux: `./build_linux.sh`

## Требования для локальной сборки

- **Windows**: Visual Studio с компонентами C++ (см. BUILD_INSTRUCTIONS.md)
- **Linux**: `rpm-build`, `python3-dev`

