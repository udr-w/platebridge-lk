$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
py -3 -m venv "$Root\backend\.venv"
& "$Root\backend\.venv\Scripts\python.exe" -m pip install -r "$Root\backend\requirements.txt"
Push-Location "$Root\frontend"; npm install; Pop-Location
Push-Location "$Root\backend"; & ".venv\Scripts\python.exe" -m app.seed; Pop-Location
Write-Host "Setup complete. Run .\scripts\start.ps1"
