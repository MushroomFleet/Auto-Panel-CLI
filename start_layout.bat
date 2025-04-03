@echo off
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo Running Comic Panel Composer...
python comic_panel_composer.py C:\vscode\web-story\siteimages\4aaa --preset presets\2col_preset.json --fit cover
echo.

pause