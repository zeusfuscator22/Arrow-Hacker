@echo off
setlocal
cd /d "%~dp0"
echo.
echo ============================================================
echo    Akatsuki 14.02 - HEN184 verified host (EXPERIMENTAL)
echo ============================================================
echo.
echo This is NOT a confirmed stable jailbreak. Kernel freezes remain possible.
echo FIRST close any older server windows (especially on port 8000).
echo.
set "PORT=%~1"
if not defined PORT set "PORT=8000"
set "PYCMD="
where py >nul 2>nul && set "PYCMD=py -3"
if not defined PYCMD (where python >nul 2>nul && set "PYCMD=python")
if not defined PYCMD (
  echo ERROR: Python 3 was not found.
  pause
  exit /b 1
)
%PYCMD% prepare_hen184.py
if errorlevel 1 (
  echo.
  echo HEN184 is MISSING or INVALID. Host has NOT started.
  echo Open this official release to download hen.bin manually:
  echo https://github.com/Scene-Collective/ps4-hen/releases/tag/pre-release-main-184
  echo Rename hen.bin to hen1402_184.bin and put it next to this BAT.
  echo.
  pause
  exit /b 2
)
echo.
echo Official HEN184 verified. Starting on port %PORT%.
echo ONLY use the fresh PS4 URL printed by THIS server window.
echo.
%PYCMD% server.py %PORT%
if errorlevel 1 (
  echo.
  echo HOST ERROR. If port 8000 is busy, close the old server
  echo or run START_HEN_1402_EXPERIMENTAL.bat 8765
)
echo.
pause
endlocal
