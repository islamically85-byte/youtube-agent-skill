# Windows Installation & Setup Guide

**YouTube Agent Studio v3.0 — Motion-First Hybrid Production Suite**
Extension Maintainer: **ABDUL MUEED LASHARY**
Original Upstream Author: **Jake Schincariol** (MIT License)

This guide provides step-by-step instructions for running YouTube Agent Studio v3.0 on Windows 10 and Windows 11.

---

## 1. Automated Quick Start (Recommended)

Run the included automated setup script in PowerShell or Command Prompt:

### Option A: Using PowerShell (Administrator recommended)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\scripts\install-motion-tools.ps1
```

### Option B: Using Windows Batch Command Prompt
```cmd
scripts\install-motion-tools.bat
```

The script automatically:
1. Detects or installs Python 3.11.
2. Installs core audio and timeline libraries (`pedalboard`, `opentimelineio`, `numpy`).
3. Installs or verifies `FFmpeg` via `winget`.
4. Detects or installs `Google Chrome` / `Microsoft Edge`.
5. Probes for `Blender LTS` 3D engine.
6. Installs verified open-source motion skills via `npx skills add`.
7. Runs system diagnostic verification.

---

## 2. Manual Prerequisites Installation

If you prefer installing tools manually:

### 1. Python 3.10+
Install via winget or the official installer:
```powershell
winget install Python.Python.3.11
```
Make sure **"Add Python to PATH"** is checked.

### 2. FFmpeg Broadcast Tools
```powershell
winget install Gyan.FFmpeg
```

### 3. Headless Browser (Chrome or Edge)
Google Chrome or Microsoft Edge (comes pre-installed with Windows):
```powershell
winget install Google.Chrome
```

### 4. Blender LTS (Optional for 3D Land Parcels)
```powershell
winget install BlenderFoundation.Blender
```

### 5. Core Python Libraries
```powershell
python -m pip install --upgrade pip
python -m pip install pedalboard opentimelineio numpy requests
```

---

## 3. Running System Readiness Diagnostics

To confirm all components are operational on Windows, run:

```powershell
# Check browser motion engine
python shared/scripts/browser_motion.py check

# Check Blender 3D procedural engine
python shared/scripts/blender_parcel_render.py check

# Check Spotify Pedalboard DSP
python shared/scripts/pedalboard_master.py check

# Check OpenTimelineIO engine
python shared/scripts/otio_export.py check
```

Expected diagnostic output:
```json
{
  "browser_found": true,
  "browser_path": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  "ffmpeg_found": true,
  "ffmpeg_path": "C:\\Program Files\\FFmpeg\\bin\\ffmpeg.exe",
  "ready": true
}
```

---

## 4. Rendering Your First 15-Second Motion Demo on Windows

```powershell
python shared/scripts/browser_motion.py render `
  --html templates/motion/discrepancy_counter.html `
  --out output/demo_motion_15s.mp4 `
  --duration 15.0 --fps 30
```

The rendered video and review contact sheet will be saved to:
- `output\demo_motion_15s.mp4`
- `output\demo_motion_15s_contact_sheet.png`
