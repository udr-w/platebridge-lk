$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Push-Location "$Root\backend"; & ".venv\Scripts\python.exe" -m app.seed; Pop-Location
