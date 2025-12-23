# build.ps1
# Build standalone executable using PyInstaller

Write-Host "`n=== Speech to Text - Build Script ===" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "[WARNING] Virtual environment not detected" -ForegroundColor Yellow
    Write-Host "          Attempting to activate..." -ForegroundColor Yellow

    if (Test-Path ".\venv\Scripts\Activate.ps1") {
        & .\venv\Scripts\Activate.ps1
        Write-Host "          [OK] Virtual environment activated" -ForegroundColor Green
    }
    else {
        Write-Host "          [ERROR] Virtual environment not found" -ForegroundColor Red
        Write-Host "          Run setup.ps1 first" -ForegroundColor Red
        exit 1
    }
}

# Check if PyInstaller is installed
Write-Host "[1/4] Checking PyInstaller..." -ForegroundColor Yellow
try {
    $pyinstallerVersion = pyinstaller --version 2>&1
    Write-Host "      [OK] PyInstaller version: $pyinstallerVersion" -ForegroundColor Green
}
catch {
    Write-Host "      [ERROR] PyInstaller not found" -ForegroundColor Red
    Write-Host "              Installing PyInstaller..." -ForegroundColor Yellow
    pip install pyinstaller
    if ($LASTEXITCODE -ne 0) {
        Write-Host "              [ERROR] Failed to install PyInstaller" -ForegroundColor Red
        exit 1
    }
}

# Clean previous builds
Write-Host "`n[2/4] Cleaning previous builds..." -ForegroundColor Yellow
if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
    Write-Host "      [OK] Removed dist folder" -ForegroundColor Green
}
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
    Write-Host "      [OK] Removed build folder" -ForegroundColor Green
}
if (Test-Path "*.spec") {
    Remove-Item -Force "*.spec"
    Write-Host "      [OK] Removed spec files" -ForegroundColor Green
}

# Build executable
Write-Host "`n[3/4] Building executable..." -ForegroundColor Yellow
Write-Host "      This may take several minutes..." -ForegroundColor Cyan

$buildCommand = "pyinstaller --onefile --windowed --name SpeechToText --clean dictation_app.py"
Write-Host "      Command: $buildCommand" -ForegroundColor Gray

Invoke-Expression $buildCommand

if ($LASTEXITCODE -ne 0) {
    Write-Host "      [ERROR] Build failed" -ForegroundColor Red
    exit 1
}

Write-Host "      [OK] Build completed" -ForegroundColor Green

# Verify executable exists
Write-Host "`n[4/4] Verifying executable..." -ForegroundColor Yellow
if (Test-Path "dist\SpeechToText.exe") {
    $fileSize = (Get-Item "dist\SpeechToText.exe").Length / 1MB
    Write-Host "      [OK] Executable created: dist\SpeechToText.exe" -ForegroundColor Green
    Write-Host "      Size: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Cyan
}
else {
    Write-Host "      [ERROR] Executable not found" -ForegroundColor Red
    exit 1
}

# Success message
Write-Host "`n=== Build Complete! ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Executable location:" -ForegroundColor White
Write-Host "  dist\SpeechToText.exe" -ForegroundColor Cyan
Write-Host ""
Write-Host "To test the executable:" -ForegroundColor White
Write-Host "  cd dist" -ForegroundColor Cyan
Write-Host "  .\SpeechToText.exe" -ForegroundColor Cyan
Write-Host ""
Write-Host "Note: First run will download Whisper model (~140MB)" -ForegroundColor Yellow
Write-Host ""

# Optional: Clean up build artifacts
$cleanup = Read-Host "Clean up build artifacts? (y/n)"
if ($cleanup -eq "y") {
    if (Test-Path "build") {
        Remove-Item -Recurse -Force "build"
    }
    if (Test-Path "*.spec") {
        Remove-Item -Force "*.spec"
    }
    Write-Host "[OK] Cleaned up build artifacts" -ForegroundColor Green
}

Write-Host ""
