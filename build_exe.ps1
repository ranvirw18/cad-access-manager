# Build CAD Institute Launcher.exe
# Run: .\build_exe.ps1

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    python -m venv .venv
}

.\.venv\Scripts\pip install -r requirements.txt -q
.\.venv\Scripts\pip install pyinstaller -q

.\.venv\Scripts\pyinstaller `
    --noconfirm `
    --onefile `
    --windowed `
    --name "CAD Institute Launcher" `
    --collect-all customtkinter `
    main.py

Write-Host ""
Write-Host "Done: dist\CAD Institute Launcher.exe" -ForegroundColor Green
