"""
Stazeni audio stopy z URL (YouTube, podcastove RSS, primy odkaz na mp3).

Zamerne se nepouziva prevod pres ffmpeg - faster-whisper dekoduje
pres PyAV, takze si poradi i s m4a/webm primo ze site.
"""

from __future__ import annotations

import threading
from pathlib import Path
from typing import Callable, Optional

from yt_dlp import YoutubeDL

ProgressFn = Callable[[str, Optional[float]], None]


class Cancelled(Exception):
    """Uzivatel prerusil beh."""


def is_url(value: str) -> bool:
    return value.strip().lower().startswith(("http://", "https://"))


def download_audio(
    url: str,
    outdir: Path,
    progress: ProgressFn,
    cancel: threading.Event,
) -> Path:
    """Stahne nejlepsi dostupnou audio stopu. Vraci cestu ke stazenemu souboru."""
    outdir.mkdir(parents=True, exist_ok=True)
    result: dict = {}

    def hook(d: dict) -> None:
        if cancel.is_set():
            raise Cancelled()

        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            done = d.get("downloaded_bytes", 0)
            pct = (done / total * 100.0) if total else None
            mb = done / 1024 / 1024
            progress(f"Stahuji audio... {mb:.1f} MB", pct)

        elif d["status"] == "finished":
            result["path"] = d.get("filename")
            progress("Audio stazeno.", 100.0)

    opts = {
        "format": "bestaudio/best",
        "outtmpl": str(outdir / "%(title).100B.%(ext)s"),
        "progress_hooks": [hook],
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,
    }

    progress("Zjistuji informace o zdroji...", None)
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)

    path = result.get("path")
    if not path:
        # zaloha, kdyby hook nedobehl (napr. soubor uz byl stazeny drive)
        path = YoutubeDL(opts).prepare_filename(info)

    return Path(path)
