@echo off
echo Creating virtual environment...
python -m venv venv
echo.

echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo Installing dependencies...
pip install -r requirements.txt
echo.

echo Creating presets directory...
if not exist presets mkdir presets
echo.

echo Setup complete! You can now run start-layout.bat to use the Comic Panel Composer.
echo.
pause