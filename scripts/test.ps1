$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Push-Location "$Root\backend"; & ".venv\Scripts\python.exe" -m pytest; Pop-Location
Push-Location "$Root\frontend"; npm test; npm run typecheck; npm run build; Pop-Location
