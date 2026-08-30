# =====================================================================
# 10000 - Sestaveni EXE pomoci PyInstaller
# =====================================================================
# Spoustet z korene projektu v aktivovanem .venv:
#   .\.venv\Scripts\Activate.ps1
#   .\build.ps1
# Vysledek: dist\Prepisovac\Prepisovac.exe
# =====================================================================

$ErrorActionPreference = "Stop"

function Write-INFO { param($m) Write-Host "[INFO] $m" -ForegroundColor Cyan }
function Write-OK   { param($m) Write-Host "[OK]   $m" -ForegroundColor Green }

Write-INFO "Kontroluji PyInstaller..."
if (-not (pip show pyinstaller 2>$null)) {
    Write-INFO "Instaluji PyInstaller..."
    pip install pyinstaller
}

Write-INFO "Cistim predchozi build..."
Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue

# ---------------------------------------------------------------------
# 20000 - Sestaveni
# ---------------------------------------------------------------------
# --onedir  : rychlejsi start nez --onefile (balik ma pres 300 MB)
# --collect-all : ctranslate2 a av maji nativni DLL, ktere PyInstaller
#                 sam nenajde; faster_whisper nese VAD model jako data
# ---------------------------------------------------------------------

Write-INFO "Sestavuji EXE (potrva nekolik minut)..."

pyinstaller `
    --name Prepisovac `
    --onedir `
    --windowed `
    --noconfirm `
    --collect-all ctranslate2 `
    --collect-all av `
    --collect-all faster_whisper `
    --collect-all tokenizers `
    --collect-all onnxruntime `
    --collect-all yt_dlp `
    src\main.py

Write-OK "Hotovo: dist\Prepisovac\Prepisovac.exe"
Write-INFO "Slozku dist\Prepisovac lze zkopirovat na jiny pocitac celou."
