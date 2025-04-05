@echo off
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo Running Comic Panel Composer...
python comic_panel_composer.py K:\MACHINES14\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\output\FODA\airship-cities-v2-e6-e3\illustration --preset presets\2col_preset.json  --fit cover --overlay frame\2col_layout_frame1.png
echo.

pause
