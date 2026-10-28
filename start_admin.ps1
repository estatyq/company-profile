$ErrorActionPreference = "Stop"

Set-Location $PSScriptRoot

if (-not (Test-Path ".\data")) {
    New-Item -ItemType Directory -Path ".\data" | Out-Null
}

Write-Host ""
Write-Host "Company Profile" -ForegroundColor Cyan
Write-Host "Admin: http://127.0.0.1:8765/admin"
Write-Host "Site:  http://127.0.0.1:8765/"
Write-Host ""

python .\app.py
