# Run the demo (Windows / PowerShell)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Resolve-Path (Join-Path $scriptDir "..")
Set-Location $projectRoot

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Secure Channel Demo - Simple Launcher" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Python check
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python is not installed or not in PATH!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python 3.10+ from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Run from repo root
if (-not (Test-Path "requirements.txt")) {
    Write-Host "[ERROR] requirements.txt not found!" -ForegroundColor Red
    Write-Host "Please run this script from the project root directory." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Dependencies
Write-Host ""
Write-Host "Checking dependencies..." -ForegroundColor Cyan
$venvDir = Join-Path $projectRoot ".venv"
$pythonExe = Join-Path $venvDir "Scripts\\python.exe"

if (-not (Test-Path $pythonExe)) {
    Write-Host "[INFO] Creating virtual environment (.venv)..." -ForegroundColor Yellow
    python -m venv $venvDir
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to create virtual environment" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

try {
    & $pythonExe -c "import flask" 2>&1 | Out-Null
    Write-Host "[OK] Dependencies already installed" -ForegroundColor Green
} catch {
    Write-Host "[INFO] Installing dependencies (this may take a minute)..." -ForegroundColor Yellow
    & $pythonExe -m pip install --upgrade pip setuptools wheel
    & $pythonExe -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to install dependencies!" -ForegroundColor Red
        Write-Host "Please check your internet connection and try again." -ForegroundColor Yellow
        Write-Host ""
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "[OK] Dependencies installed successfully!" -ForegroundColor Green
}

# Sanity checks
if (-not (Test-Path "frontend")) {
    Write-Host "[ERROR] frontend directory not found!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

if (-not (Test-Path "backend\app.py")) {
    Write-Host "[ERROR] app.py not found in backend directory!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Starting Flask server..." -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
$port = if ($env:PORT) { [int]$env:PORT } else { 5000 }
Write-Host "The server will start at: http://localhost:$port" -ForegroundColor Green
Write-Host ""
Write-Host "Your browser should open automatically." -ForegroundColor Yellow
Write-Host "If not, manually open: http://localhost:$port" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Open the browser
Start-Sleep -Seconds 3
Start-Process "http://localhost:$port"

# Start server
Set-Location backend
$env:PORT = "$port"
& $pythonExe app.py

