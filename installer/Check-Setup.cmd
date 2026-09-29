@echo off
echo Thor Forever - read-only setup check
echo No game settings or components will be changed.
start.exe /unix /system/bin/sh /sdcard/Download/Thor-Forever/installer/check-setup.sh
echo Wait five seconds, then open setup-check.txt in the installer folder.
pause
