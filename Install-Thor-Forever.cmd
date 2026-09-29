@echo off
echo Thor Forever - separate installation
echo Close WoW and Battle.net before proceeding. Your game must already be installed.
echo This creates a separate runtime, prefix and settings. Shared game Data is not read-only.
echo Leave this container open. Preparation can take several minutes.
pause
start.exe /unix /system/bin/sh /sdcard/Download/Thor-Forever/installer/setup.sh
echo Open the setup-report folder to see the result. Do not run installation repeatedly.
pause
