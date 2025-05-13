@echo off
echo Starte Installation der Python-Pakete...

:: Stelle sicher, dass pip funktioniert
python -m pip install --upgrade pip

:: Installiere die gewünschten Pakete
python -m pip install requests pyinstaller

echo.
echo Fertig! Drücke eine Taste zum Beenden.
pause
