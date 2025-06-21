@ECHO off

cd %~dp0

pyrcc5.exe -o images_qr.py images.qrc
pyinstaller.exe --icon=.\icon.ico --noconsole -F .\ESL.py
