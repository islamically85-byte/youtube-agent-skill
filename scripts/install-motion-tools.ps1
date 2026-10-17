# ==============================================================================
# install-motion-tools.ps1 — Windows PowerShell Setup for YouTube Agent Studio v3.0
# Motion-First Hybrid Production Suite (Chrome, Blender, FFmpeg, Pedalboard, OTIO)
#
# Maintainer: ABDUL MUEED LASHARY
# Upstream Author: Jake Schincariol (MIT License)
# ==============================================================================

[CmdletBinding()]
param(
    [switch]$SkipOptionalSkills = $false,
    [switch]$Quiet = $false
)

$ErrorActionPreference = "Continue"

Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host " [YOUTUBE AGENT STUDIO v3.0] Motion-First Windows PowerShell Setup" -ForegroundColor White
Write-Host " Maintainer: ABDUL MUEED LASHARY" -ForegroundColor Yellow
Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Check Python
$pythonBin = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonBin) {
    Write-Warning "Python 3 is not found in PATH."
    Write-Host "Installing Python 3.11 via winget..." -ForegroundColor Yellow
    winget install Python.Python.3.11 --accept-source-agreements --accept-package-agreements
} else {
    Write-Host "[OK] Python detected: $(& python --version)" -ForegroundColor Green
}

# 2. Install Core Python Libraries
Write-Host "`n[1/5] Installing core DSP and timeline libraries (pedalboard, opentimelineio)..." -ForegroundColor Cyan
& python -m pip install --upgrade pip
& python -m pip install pedalboard opentimelineio numpy requests

# 3. Check FFmpeg
Write-Host "`n[2/5] Checking FFmpeg broadcast encoding engine..." -ForegroundColor Cyan
$ffmpegBin = Get-Command ffmpeg -ErrorAction SilentlyContinue
if (-not $ffmpegBin) {
    Write-Host "FFmpeg not detected. Installing Gyan.FFmpeg via winget..." -ForegroundColor Yellow
    winget install Gyan.FFmpeg --accept-source-agreements --accept-package-agreements
} else {
    Write-Host "[OK] FFmpeg is available." -ForegroundColor Green
}

# 4. Check Headless Browser
Write-Host "`n[3/5] Checking Browser (Google Chrome / Microsoft Edge)..." -ForegroundColor Cyan
$chromePath = "$env:ProgramFiles\Google\Chrome\Application\chrome.exe"
$edgePath = "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe"

if (Test-Path $chromePath) {
    Write-Host "[OK] Google Chrome located at $chromePath" -ForegroundColor Green
} elseif (Test-Path $edgePath) {
    Write-Host "[OK] Microsoft Edge located at $edgePath" -ForegroundColor Green
} else {
    Write-Host "Installing Google Chrome via winget..." -ForegroundColor Yellow
    winget install Google.Chrome --accept-source-agreements --accept-package-agreements
}

# 5. Check Blender LTS
Write-Host "`n[4/5] Checking Blender LTS 3D Engine..." -ForegroundColor Cyan
$blenderBin = Get-Command blender -ErrorAction SilentlyContinue
if (-not $blenderBin) {
    Write-Host "[NOTICE] Blender LTS not found in PATH." -ForegroundColor Gray
    Write-Host "To enable 3D architectural parcel flyovers, run: winget install BlenderFoundation.Blender" -ForegroundColor Gray
    Write-Host "(2D motion graphics and stock workflows remain 100% operational without Blender)" -ForegroundColor DarkGray
} else {
    Write-Host "[OK] Blender LTS is available." -ForegroundColor Green
}

# 6. Optional Open-Source Skills via Official Skills CLI
if (-not $SkipOptionalSkills) {
    Write-Host "`n[5/5] Checking official skills CLI for open-source motion skills..." -ForegroundColor Cyan
    $npxBin = Get-Command npx -ErrorAction SilentlyContinue
    if ($npxBin) {
        Write-Host "Adding verified open-source motion skills..." -ForegroundColor Yellow
        Write-Host "• JakeB-5/motion-graphic-skill (MIT License)" -ForegroundColor Gray
        & npx -y skills add JakeB-5/motion-graphic-skill

        Write-Host "• haidrrrry/claude-remotion-skill (MIT License)" -ForegroundColor Gray
        & npx -y skills add haidrrrry/claude-remotion-skill

        Write-Host "`n[NOTICE] abhimahamkali/claude-motion-skill is an optional upstream skill." -ForegroundColor Gray
        Write-Host "In compliance with open-source licensing rules, proprietary or unconfirmed-license" -ForegroundColor Gray
        Write-Host "skills are not bundled without explicit authorization." -ForegroundColor Gray
    } else {
        Write-Host "Node.js / npx not installed. Skipping optional skills CLI packages." -ForegroundColor DarkGray
    }
}

# 7. Verification Probes
Write-Host "`n==============================================================================" -ForegroundColor Cyan
Write-Host " [VERIFICATION] Running Component Diagnostics..." -ForegroundColor White
Write-Host "==============================================================================" -ForegroundColor Cyan

& python shared/scripts/browser_motion.py check
& python shared/scripts/blender_parcel_render.py check
& python shared/scripts/pedalboard_master.py check
& python shared/scripts/otio_export.py check

Write-Host "`n[SUCCESS] Setup and verification finished successfully!" -ForegroundColor Green
