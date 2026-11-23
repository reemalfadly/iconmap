# iconMap one-step setup (Windows PowerShell). Run: powershell -ExecutionPolicy Bypass -File setup.ps1
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
Write-Host "iconMap setup"
if (-not (Get-Command node -ErrorAction SilentlyContinue)) { winget install -e --id OpenJS.NodeJS.LTS; Write-Host "Node installed - close and reopen PowerShell, then run this again."; exit }
Write-Host "  OK Node $(node -v)"
if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) { winget install -e --id Gyan.FFmpeg; Write-Host "ffmpeg installed - reopen PowerShell, then run this again."; exit }
Write-Host "  OK ffmpeg"
if (-not (Get-Command python -ErrorAction SilentlyContinue)) { Write-Host "Install Python 3.10 or newer from https://python.org, then run this again."; exit }
Write-Host "  OK $(python --version)"
npm install --silent; npx playwright install chromium
Write-Host "  OK Playwright and Chromium"
python -m pip install -q -r requirements.txt
Write-Host "  OK Python packages (voice, timing, imagery, mix)"
node scripts/render.mjs examples/demo-ar.json test-render.mp4 --scale 0.5 --to 3
Write-Host "Done! test-render.mp4 created. The Globe engine (real NASA imagery, 3D) needs a GPU with WebGL: see README."