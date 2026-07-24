$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Backend = Start-Process -PassThru -WorkingDirectory "$Root\backend" -FilePath "$Root\backend\.venv\Scripts\python.exe" -ArgumentList "-m","uvicorn","app.main:app","--reload","--port","8000"
$Frontend = Start-Process -PassThru -WorkingDirectory "$Root\frontend" -FilePath "npm.cmd" -ArgumentList "run","dev"
Write-Host "PlateBridge LK: http://localhost:5173 (Ctrl+C to stop)"
try { Wait-Process -Id $Backend.Id,$Frontend.Id } finally { Stop-Process -Id $Backend.Id,$Frontend.Id -Force -ErrorAction SilentlyContinue }
