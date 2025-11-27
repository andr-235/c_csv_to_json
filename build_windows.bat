@echo off
echo Building Windows .exe...
echo.
echo NOTE: Для сборки Windows приложения нужны компоненты Visual Studio:
echo   - MSVC v142 - VS 2019 C++ x64/x86 build tools
echo   - C++ CMake tools for Windows
echo   - Windows 10 SDK
echo.
echo Запускаю сборку...
echo.

cd /d "%~dp0"
call venv\Scripts\activate.bat
flet build windows

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Build complete! Check build/flutter/windows/build/runner/Release/ folder
) else (
    echo.
    echo Build failed! Check errors above.
    echo.
    echo Если видите ошибку о Visual Studio, установите необходимые компоненты:
    echo https://visualstudio.microsoft.com/downloads/
    echo.
)

pause

