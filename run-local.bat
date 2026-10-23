@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if not errorlevel 1 (
  py -3 portable\launch_v16.py %*
) else (
  where python >nul 2>nul
  if not errorlevel 1 (
    python portable\launch_v16.py %*
  ) else (
    echo Python 3.10 or newer is required. Install Python and run this file again.
    exit /b 1
  )
)
endlocal
