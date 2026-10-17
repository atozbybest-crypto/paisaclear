@echo off
setlocal
cd /d "%~dp0"

set "PY="
where py >nul 2>nul
if not errorlevel 1 set "PY=py"

if not defined PY (
  where python >nul 2>nul
  if not errorlevel 1 set "PY=python"
)

if not defined PY (
  set "CAND=%USERPROFILE%\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe"
  if exist "%CAND%" set "PY=%CAND%"
)

if not defined PY (
  echo.
  echo   Python was not found on this machine.
  echo.
  echo   You do not need it: double-click PaisaClear.html instead.
  echo   That file is the whole site and needs nothing installed.
  echo.
  pause
  exit /b 1
)

"%PY%" serve.py
if errorlevel 1 pause
