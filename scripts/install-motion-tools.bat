@echo off
REM ==============================================================================
REM install-motion-tools.bat — Windows Installation for YouTube Agent Studio v3.0
REM Motion-First Hybrid Production Suite (Chrome, Blender, FFmpeg, Pedalboard, OTIO)
REM 
REM Maintainer: ABDUL MUEED LASHARY
REM Upstream Author: Jake Schincariol (MIT License)
REM ==============================================================================

setlocal enabledelayedexpansion
echo ==============================================================================
echo [YOUTUBE AGENT STUDIO v3.0] Motion-First Windows Installation
echo Maintainer: ABDUL MUEED LASHARY
echo ==============================================================================
echo.

REM 1. Python Environment Check
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python 3 is not installed or not in your PATH!
    echo Please install Python 3.10+ from https://www.python.org or via:
    echo   winget install Python.Python.3.11
    pause
    exit /b 1
)
echo [OK] Python detected:
python --version

REM 2. Install Python Core Libraries
echo.
echo [1/5] Installing core audio and timeline dependencies...
python -m pip install --upgrade pip
python -m pip install pedalboard opentimelineio numpy requests

REM 3. FFmpeg Verification
echo.
echo [2/5] Checking FFmpeg...
where ffmpeg >nul 2>nul
if %errorlevel% neq 0 (
    echo [NOTICE] FFmpeg not found on PATH. Attempting automated installation via winget...
    winget install Gyan.FFmpeg --accept-source-agreements --accept-package-agreements
    echo If winget requires a terminal restart, please reopen this terminal afterwards.
) else (
    echo [OK] FFmpeg is already installed:
    ffmpeg -version | findstr /i "version"
)

REM 4. Headless Browser (Google Chrome / Microsoft Edge)
echo.
echo [3/5] Checking Browser (Chrome / Edge)...
where chrome >nul 2>nul
if %errorlevel% neq 0 (
    where msedge >nul 2>nul
    if %errorlevel% neq 0 (
        echo [NOTICE] Chrome/Edge not found in PATH. Checking Program Files...
        if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" (
            echo [OK] Chrome found in Program Files.
        ) else if exist "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" (
            echo [OK] Edge found in Program Files (x86).
        ) else (
            echo [NOTICE] Installing Google Chrome via winget...
            winget install Google.Chrome --accept-source-agreements --accept-package-agreements
        )
    ) else (
        echo [OK] Microsoft Edge detected.
    )
) else (
    echo [OK] Google Chrome detected.
)

REM 5. Blender LTS 3D Engine
echo.
echo [4/5] Checking Blender LTS...
where blender >nul 2>nul
if %errorlevel% neq 0 (
    if exist "%ProgramFiles%\Blender Foundation\Blender 4.2\blender.exe" (
        echo [OK] Blender found at %ProgramFiles%\Blender Foundation\Blender 4.2\blender.exe
    ) else if exist "%ProgramFiles%\Blender Foundation\Blender 5.2\blender.exe" (
        echo [OK] Blender found at %ProgramFiles%\Blender Foundation\Blender 5.2\blender.exe
    ) else (
        echo [NOTICE] Blender LTS not found. You can install it via winget:
        echo   winget install BlenderFoundation.Blender
        echo (Blender is optional for 3D parcels; 2D motion graphics remain fully functional)
    )
) else (
    echo [OK] Blender detected on PATH:
    blender --version | findstr /i "Blender"
)

REM 6. Optional Open-Source Skills via Official Skills CLI
echo.
echo [5/5] Checking Skills CLI for optional motion skills...
where npx >nul 2>nul
if %errorlevel% equ 0 (
    echo Installing verified MIT-licensed motion skills...
    echo - JakeB-5/motion-graphic-skill (MIT)
    call npx -y skills add JakeB-5/motion-graphic-skill
    echo - haidrrrry/claude-remotion-skill (MIT)
    call npx -y skills add haidrrrry/claude-remotion-skill
    echo.
    echo [NOTICE] abhimahamkali/claude-motion-skill is an optional upstream skill.
    echo In accordance with copyright compliance, proprietary or unconfirmed-license
    echo repositories are not automatically bundled without license authorization.
) else (
    echo [NOTICE] Node.js / npx not found. Skipping optional skills CLI add-ons.
)

REM 7. Run Verification Probes
echo.
echo ==============================================================================
echo [VERIFICATION] Testing YouTube Agent Studio v3.0 Components...
echo ==============================================================================
python shared\scripts\browser_motion.py check
python shared\scripts\blender_parcel_render.py check
python shared\scripts\pedalboard_master.py check
python shared\scripts\otio_export.py check

echo.
echo ==============================================================================
echo [SUCCESS] Windows installation and component verification complete!
echo ==============================================================================
pause
