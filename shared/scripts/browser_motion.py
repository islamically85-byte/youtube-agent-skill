#!/usr/bin/env python3
"""
browser_motion.py — Deterministic Browser-Based Motion Graphics Engine
Part of YouTube Agent Studio v3.0

Renders HTML5/Canvas/SVG/CSS scenes into professional broadcast-quality MP4/MOV/WebM
using headless Chrome/Edge and FFmpeg.

Author: ABDUL MUEED LASHARY
Upstream: Jake Schincariol (MIT License)
"""

import argparse
import http.server
import json
import os
import platform
import shutil
import socketserver
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT_DIR = Path(__file__).resolve().parent.parent.parent


def find_system_browser() -> Optional[str]:
    """Auto-detect Google Chrome, Microsoft Edge, or Chromium on macOS, Windows, and Linux."""
    system = platform.system().lower()

    # Priority 1: User or environment override
    custom_path = os.environ.get("BROWSER_PATH") or os.environ.get("CHROME_PATH")
    if custom_path and os.path.exists(custom_path):
        return custom_path

    # Priority 2: System PATH lookups
    for bin_name in ["google-chrome", "chromium", "chromium-browser", "chrome", "msedge"]:
        path = shutil.which(bin_name)
        if path:
            return path

    # Priority 3: OS-specific standard installation locations
    candidates = []
    if system == "darwin":
        candidates = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
            os.path.expanduser("~/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        ]
    elif system == "windows":
        prog_files = os.environ.get("PROGRAMFILES", r"C:\Program Files")
        prog_files_x86 = os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)")
        local_app = os.environ.get("LOCALAPPDATA", "")
        candidates = [
            os.path.join(prog_files, r"Google\Chrome\Application\chrome.exe"),
            os.path.join(prog_files_x86, r"Google\Chrome\Application\chrome.exe"),
            os.path.join(local_app, r"Google\Chrome\Application\chrome.exe"),
            os.path.join(prog_files, r"Microsoft\Edge\Application\msedge.exe"),
            os.path.join(prog_files_x86, r"Microsoft\Edge\Application\msedge.exe"),
        ]
    else:  # Linux / Unix
        candidates = [
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable",
            "/usr/bin/chromium",
            "/usr/bin/chromium-browser",
            "/snap/bin/chromium",
        ]

    for p in candidates:
        if p and os.path.exists(p):
            return p

    return None


def find_ffmpeg() -> Optional[str]:
    """Locate FFmpeg executable."""
    custom = os.environ.get("FFMPEG_PATH")
    if custom and os.path.exists(custom):
        return custom
    return shutil.which("ffmpeg")


def get_aspect_dimensions(aspect: str, custom_w: Optional[int] = None, custom_h: Optional[int] = None) -> Tuple[int, int]:
    """Resolve width and height from standard aspect ratios."""
    if custom_w and custom_h:
        return custom_w, custom_h
    aspect_map = {
        "16:9": (1920, 1080),
        "9:16": (1080, 1920),
        "1:1": (1080, 1080),
        "4:5": (1080, 1350),
        "4:3": (1440, 1080),
    }
    return aspect_map.get(aspect, (1920, 1080))


class StreamingFrameServer:
    """Ultra-fast local HTTP server receiving Canvas blobs from headless Chrome."""

    def __init__(self, html_path: Path, frames_dir: Path, total_frames: int, fps: int, width: int, height: int, is_transparent: bool):
        self.html_path = html_path
        self.frames_dir = frames_dir
        self.total_frames = total_frames
        self.fps = fps
        self.width = width
        self.height = height
        self.is_transparent = is_transparent
        self.received_frames = 0
        self.is_done = False
        self.httpd = None
        self.port = 0
        self.server_thread = None

    def start(self):
        parent = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_OPTIONS(self):
                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
                self.send_header("Access-Control-Allow-Headers", "*")
                self.end_headers()

            def do_GET(self):
                # Serve the HTML page with injected streaming harness
                try:
                    raw_html = parent.html_path.read_text(encoding="utf-8")
                except Exception as e:
                    self.send_error(500, f"Cannot read HTML file: {e}")
                    return

                mime_ext = "image/png" if parent.is_transparent else "image/jpeg"
                quality = 0.95

                harness = f"""
                <script>
                (function() {{
                  async function startStreaming() {{
                    const c = document.getElementById('motionCanvas') || document.querySelector('canvas');
                    if (!c) {{
                      console.error('No canvas found for streaming');
                      return;
                    }}
                    c.width = {parent.width};
                    c.height = {parent.height};
                    const total = {parent.total_frames};
                    const fps = {parent.fps};

                    for (let f = 0; f < total; f++) {{
                      if (window.renderFrame) {{
                        window.renderFrame(f, total, fps);
                      }}
                      const blob = await new Promise(res => c.toBlob(res, '{mime_ext}', {quality}));
                      await fetch('/frame?n=' + f, {{
                        method: 'POST',
                        body: blob
                      }});
                    }}
                    await fetch('/done', {{ method: 'POST', body: 'done' }});
                  }}
                  if (document.readyState === 'complete') {{
                    startStreaming();
                  }} else {{
                    window.addEventListener('load', startStreaming);
                  }}
                }})();
                </script>
                """

                # Inject harness before </body> or append
                if "</body>" in raw_html:
                    served_html = raw_html.replace("</body>", f"{harness}</body>")
                else:
                    served_html = raw_html + harness

                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(served_html.encode("utf-8"))

            def do_POST(self):
                if "/done" in self.path:
                    parent.is_done = True
                    self.send_response(200)
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(b'{"status": "complete"}')
                    return

                if "/frame" in self.path:
                    # Parse frame index
                    query = self.path.split("?", 1)[-1] if "?" in self.path else ""
                    frame_num = parent.received_frames
                    for part in query.split("&"):
                        if part.startswith("n="):
                            try:
                                frame_num = int(part.split("=")[1])
                            except ValueError:
                                pass

                    length = int(self.headers.get("Content-Length", 0))
                    data = self.rfile.read(length)
                    ext = "png" if parent.is_transparent else "jpg"
                    frame_file = parent.frames_dir / f"frame_{frame_num:05d}.{ext}"
                    frame_file.write_bytes(data)
                    parent.received_frames += 1

                    self.send_response(200)
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(b'{"status": "ok"}')
                    return

                self.send_response(404)
                self.end_headers()

            def log_message(self, format, *args):
                pass  # Suppress HTTP server noise

        self.httpd = socketserver.TCPServer(("127.0.0.1", 0), Handler)
        self.port = self.httpd.server_address[1]
        self.server_thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.server_thread.start()

    def stop(self):
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()


def render_html_motion(
    html_path: str,
    output_path: str,
    duration: float = 15.0,
    fps: int = 30,
    aspect: str = "16:9",
    width: Optional[int] = None,
    height: Optional[int] = None,
    transparent: bool = False,
    generate_contact_sheet: bool = True,
    generate_previews: bool = True,
    browser_bin: Optional[str] = None,
    ffmpeg_bin: Optional[str] = None,
    timeout: int = 180,
) -> Dict[str, any]:
    """
    Render an HTML animation to video using headless browser capture and FFmpeg.

    Returns a manifest dictionary containing paths to video, thumbnails, contact sheet, and metrics.
    """
    html_file = Path(html_path).resolve()
    if not html_file.exists():
        raise FileNotFoundError(f"Source HTML animation file not found: {html_file}")

    browser = browser_bin or find_system_browser()
    if not browser:
        raise RuntimeError(
            "Headless browser not found! Please install Google Chrome, Microsoft Edge, or Chromium."
        )

    ffmpeg = ffmpeg_bin or find_ffmpeg()
    if not ffmpeg:
        raise RuntimeError("FFmpeg executable not found in PATH or environment!")

    w, h = get_aspect_dimensions(aspect, width, height)
    total_frames = int(round(duration * fps))
    out_file = Path(output_path).resolve()
    out_file.parent.mkdir(parents=True, exist_ok=True)

    t_start = time.time()
    frames_dir_obj = tempfile.TemporaryDirectory(prefix="motion_frames_")
    frames_dir = Path(frames_dir_obj.name)

    print(f"[BROWSER-MOTION] Target: {out_file.name}")
    print(f"[BROWSER-MOTION] Dimensions: {w}x{h} ({aspect}) | Duration: {duration}s | FPS: {fps} | Frames: {total_frames}")
    print(f"[BROWSER-MOTION] Browser: {browser}")

    server = StreamingFrameServer(
        html_path=html_file,
        frames_dir=frames_dir,
        total_frames=total_frames,
        fps=fps,
        width=w,
        height=h,
        is_transparent=transparent,
    )
    server.start()

    # Launch Chrome headlessly to stream frames
    chrome_cmd = [
        browser,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--hide-scrollbars",
        f"--window-size={w},{h}",
        f"http://127.0.0.1:{server.port}/",
    ]

    proc = subprocess.Popen(chrome_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Wait for completion or timeout
    deadline = time.time() + timeout
    last_count = 0
    while not server.is_done and time.time() < deadline:
        time.sleep(0.1)
        if server.received_frames != last_count and server.received_frames % 30 == 0:
            pct = round((server.received_frames / total_frames) * 100, 1)
            print(f"  ... rendering frames: {server.received_frames}/{total_frames} ({pct}%)")
            last_count = server.received_frames

    # Clean up browser and server
    try:
        proc.terminate()
        proc.wait(timeout=2)
    except Exception:
        proc.kill()
    server.stop()

    actual_frames = len(list(frames_dir.glob("frame_*.*")))
    capture_time = time.time() - t_start
    print(f"[BROWSER-MOTION] Captured {actual_frames}/{total_frames} frames in {capture_time:.2f}s ({actual_frames/capture_time:.1f} fps)")

    if actual_frames < total_frames * 0.9:
        frames_dir_obj.cleanup()
        raise RuntimeError(f"Browser capture aborted early: only {actual_frames}/{total_frames} frames received.")

    # Determine frame extension
    ext = "png" if transparent else "jpg"
    input_pattern = str(frames_dir / f"frame_%05d.{ext}")

    # Build FFmpeg command based on format and transparency
    is_mov = out_file.suffix.lower() == ".mov"
    is_webm = out_file.suffix.lower() == ".webm"

    ffmpeg_cmd = [ffmpeg, "-y", "-r", str(fps), "-i", input_pattern]

    if transparent:
        if is_mov:
            ffmpeg_cmd.extend(["-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le"])
        elif is_webm:
            ffmpeg_cmd.extend(["-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "2M"])
        else:
            ffmpeg_cmd.extend(["-c:v", "png"])
    else:
        ffmpeg_cmd.extend([
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-crf", "18",
            "-preset", "fast",
            "-movflags", "+faststart",
        ])

    ffmpeg_cmd.append(str(out_file))

    print(f"[BROWSER-MOTION] Encoding with FFmpeg -> {out_file.name}")
    res = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        frames_dir_obj.cleanup()
        raise RuntimeError(f"FFmpeg encoding failed: {res.stderr}")

    total_time = time.time() - t_start
    file_size_mb = out_file.stat().st_size / (1024 * 1024)
    print(f"[BROWSER-MOTION] Render complete in {total_time:.2f}s! Output size: {file_size_mb:.2f} MB")

    # Generate contact sheet and review thumbnails if requested
    contact_sheet_path = None
    preview_thumbnails = []

    if generate_contact_sheet or generate_previews:
        sample_indices = [
            0,
            int(total_frames * 0.15),
            int(total_frames * 0.35),
            int(total_frames * 0.50),
            int(total_frames * 0.65),
            int(total_frames * 0.85),
            max(0, total_frames - 1),
        ]

        preview_dir = out_file.parent / "previews"
        preview_dir.mkdir(parents=True, exist_ok=True)

        for idx in sample_indices:
            src_frame = frames_dir / f"frame_{idx:05d}.{ext}"
            if src_frame.exists():
                thumb_name = f"{out_file.stem}_frame_{idx:04d}.{ext}"
                dest_thumb = preview_dir / thumb_name
                shutil.copy2(src_frame, dest_thumb)
                preview_thumbnails.append(str(dest_thumb))

        if generate_contact_sheet and len(preview_thumbnails) >= 4:
            contact_sheet_file = out_file.parent / f"{out_file.stem}_contact_sheet.png"
            # Build 3x2 or 4x2 contact sheet using FFmpeg tile filter
            tile_inputs = [preview_dir / f"{out_file.stem}_frame_{idx:04d}.{ext}" for idx in sample_indices[:6]]
            existing_tiles = [p for p in tile_inputs if p.exists()]
            if existing_tiles:
                cs_cmd = [ffmpeg, "-y"]
                for p in existing_tiles:
                    cs_cmd.extend(["-i", str(p)])
                filter_desc = f"scale=640:360,hstack=inputs=3[top];scale=640:360,hstack=inputs=3[bot];[top][bot]vstack=inputs=2" if len(existing_tiles) == 6 else "scale=640:360"
                # Simpler robust tile using ffmpeg -filter_complex
                cs_cmd.extend([
                    "-filter_complex",
                    f"nullsrc=size=1920:720[base];" +
                    "".join([f"[{i}:v]scale=640:360[v{i}];" for i in range(len(existing_tiles))]) +
                    "".join([f"[base][v{i}]overlay={ (i % 3) * 640 }:{ (i // 3) * 360 }" + (f"[tmp{i}];[tmp{i}]" if i < len(existing_tiles)-1 else "") for i in range(len(existing_tiles))]),
                    "-frames:v", "1",
                    str(contact_sheet_file)
                ])
                try:
                    subprocess.run(cs_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                    if contact_sheet_file.exists():
                        contact_sheet_path = str(contact_sheet_file)
                except Exception:
                    # Fallback copy one representative frame
                    if preview_thumbnails:
                        shutil.copy2(preview_thumbnails[len(preview_thumbnails)//2], contact_sheet_file)
                        contact_sheet_path = str(contact_sheet_file)

    frames_dir_obj.cleanup()

    manifest = {
        "status": "success",
        "video_path": str(out_file),
        "file_size_mb": round(file_size_mb, 2),
        "duration_sec": duration,
        "fps": fps,
        "resolution": f"{w}x{h}",
        "aspect_ratio": aspect,
        "total_frames": total_frames,
        "render_time_sec": round(total_time, 2),
        "contact_sheet": contact_sheet_path,
        "preview_thumbnails": preview_thumbnails,
        "maintainer": "ABDUL MUEED LASHARY",
        "license": "MIT",
    }
    return manifest


def main():
    parser = argparse.ArgumentParser(description="Deterministic Browser-Based Motion Graphics Engine")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Render command
    render_p = subparsers.add_parser("render", help="Render an HTML animation to video")
    render_p.add_argument("--html", required=True, help="Path to source HTML animation")
    render_p.add_argument("--out", required=True, help="Output video file (.mp4, .mov, .webm)")
    render_p.add_argument("--duration", type=float, default=15.0, help="Duration in seconds (default: 15.0)")
    render_p.add_argument("--fps", type=int, default=30, help="Framerate (default: 30)")
    render_p.add_argument("--aspect", choices=["16:9", "9:16", "1:1", "4:5", "4:3"], default="16:9", help="Aspect ratio")
    render_p.add_argument("--width", type=int, help="Custom width in pixels")
    render_p.add_argument("--height", type=int, help="Custom height in pixels")
    render_p.add_argument("--transparent", action="store_true", help="Render with alpha transparency")
    render_p.add_argument("--no-contact-sheet", action="store_true", help="Skip contact sheet generation")
    render_p.add_argument("--json", action="store_true", help="Output JSON result manifest")

    # Check command
    check_p = subparsers.add_parser("check", help="Check system browser and FFmpeg readiness")

    # List templates
    list_p = subparsers.add_parser("templates", help="List available motion graphic templates")

    args = parser.parse_args()

    if args.command == "check":
        browser = find_system_browser()
        ffmpeg = find_ffmpeg()
        status = {
            "browser_found": bool(browser),
            "browser_path": browser,
            "ffmpeg_found": bool(ffmpeg),
            "ffmpeg_path": ffmpeg,
            "os": platform.system(),
            "ready": bool(browser and ffmpeg),
        }
        print(json.dumps(status, indent=2))
        sys.exit(0 if status["ready"] else 1)

    elif args.command == "templates":
        templates_dir = ROOT_DIR / "templates" / "motion"
        tpls = list(templates_dir.glob("*.html")) if templates_dir.exists() else []
        print(f"Available motion templates ({len(tpls)}):")
        for t in tpls:
            print(f"  - {t.name} ({t.stat().st_size} bytes)")
        sys.exit(0)

    elif args.command == "render":
        try:
            res = render_html_motion(
                html_path=args.html,
                output_path=args.out,
                duration=args.duration,
                fps=args.fps,
                aspect=args.aspect,
                width=args.width,
                height=args.height,
                transparent=args.transparent,
                generate_contact_sheet=not args.no_contact_sheet,
            )
            if args.json:
                print(json.dumps(res, indent=2))
            else:
                print("\n[SUCCESS] Video rendered successfully:")
                print(f"  Output: {res['video_path']}")
                print(f"  Size: {res['file_size_mb']} MB")
                print(f"  Duration: {res['duration_sec']}s @ {res['fps']} FPS ({res['resolution']})")
                if res.get("contact_sheet"):
                    print(f"  Contact Sheet: {res['contact_sheet']}")
        except Exception as e:
            print(f"[ERROR] Motion render failed: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
