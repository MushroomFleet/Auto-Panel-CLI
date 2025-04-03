@echo off
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo Running Comic Panel Composer...
python comic_panel_composer.py %*
echo.

pause