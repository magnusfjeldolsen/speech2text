# setup.ps1
# Oppsett av Python virtual environment og installasjon av dependencies

Write-Host "`n=== Speech to Text - Setup Script ===" -ForegroundColor Cyan
Write-Host ""

# 1. Sjekk Python
Write-Host "[1/5] Sjekker Python-installasjon..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "      [OK] Fant $pythonVersion" -ForegroundColor Green
    }
    else {
        throw "Python not found"
    }
}
catch {
    Write-Host "      [ERROR] Python er ikke installert eller ikke i PATH" -ForegroundColor Red
    Write-Host "              Last ned Python fra https://www.python.org/downloads/" -ForegroundColor Red
    exit 1
}

# 2. Opprett venv hvis den ikke finnes
Write-Host "`n[2/5] Oppretter virtual environment..." -ForegroundColor Yellow
if (-Not (Test-Path "venv")) {
    python -m venv venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "      [OK] Virtual environment opprettet" -ForegroundColor Green
    }
    else {
        Write-Host "      [ERROR] Kunne ikke opprette virtual environment" -ForegroundColor Red
        exit 1
    }
}
else {
    Write-Host "      [OK] Virtual environment finnes allerede" -ForegroundColor Green
}

# 3. Aktiver venv
Write-Host "`n[3/5] Aktiverer virtual environment..." -ForegroundColor Yellow
try {
    & .\venv\Scripts\Activate.ps1
    Write-Host "      [OK] Virtual environment aktivert" -ForegroundColor Green
}
catch {
    Write-Host "      [ERROR] Kunne ikke aktivere virtual environment" -ForegroundColor Red
    Write-Host "              Prøv å kjøre: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
    exit 1
}

# 4. Oppgrader pip
Write-Host "`n[4/5] Oppgraderer pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "      [OK] pip oppgradert" -ForegroundColor Green
}
else {
    Write-Host "      [WARNING] pip-oppgradering feilet, fortsetter likevel..." -ForegroundColor Yellow
}

# 5. Installer requirements
Write-Host "`n[5/5] Installerer dependencies..." -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
    if ($LASTEXITCODE -eq 0) {
        Write-Host "      [OK] Alle dependencies installert" -ForegroundColor Green
    }
    else {
        Write-Host "      [ERROR] Noen dependencies feilet" -ForegroundColor Red
        exit 1
    }
}
else {
    Write-Host "      [ERROR] Fant ikke requirements.txt" -ForegroundColor Red
    exit 1
}

# Ferdig
Write-Host "`n=== Setup Fullført! ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Virtual environment er aktivt (se '(venv)' i prompten)" -ForegroundColor Green
Write-Host ""
Write-Host "Kjør applikasjonen med:" -ForegroundColor White
Write-Host "  python dictation_app.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "Ved første kjøring vil Whisper-modellen (~140MB) lastes ned automatisk." -ForegroundColor Yellow
Write-Host ""
