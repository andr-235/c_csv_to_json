# Инструкции по сборке

## Windows (.exe)

1. Активируйте виртуальное окружение:
```bash
.\venv\Scripts\Activate.ps1
```

2. Установите зависимости (если еще не установлены):
```bash
pip install flet
```

3. Запустите сборку:
```bash
build_windows.bat
```
или
```bash
flet build windows
```

Результат будет в папке `build/windows/`

## Linux Fedora (.rpm)

1. Активируйте виртуальное окружение:
```bash
source venv/bin/activate
```

2. Установите briefcase:
```bash
pip install briefcase
```

3. Установите системные зависимости (Fedora):
```bash
sudo dnf install rpm-build python3-devel
```

4. Запустите сборку:
```bash
chmod +x build_linux.sh
./build_linux.sh
```
или вручную:
```bash
briefcase create
briefcase build
briefcase package --format rpm
```

Результат будет в папке `dist/`

## Запуск приложения в режиме разработки

```bash
py src/csvjsonapp/app.py
```
или
```bash
flet run src/csvjsonapp/app.py
```

