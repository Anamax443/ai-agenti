"""
Prevod audia na text pomoci faster-whisper.

Model se nacita jednou a drzi v pameti - opakovany prepis je proto
podstatne rychlejsi nez spousteni CLI pro kazdy soubor zvlast.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

from faster_whisper import WhisperModel

# Callback pro hlaseni stavu: (text_do_status_baru, procenta_nebo_None)
ProgressFn = Callable[[str, Optional[float]], None]


class Cancelled(Exception):
    """Uzivatel prerusil beh."""


@dataclass
class TranscribeOptions:
    model_size: str = "medium"      # tiny | base | small | medium | large-v3 | large-v3-turbo
    language: str = "cs"            # None = autodetekce
    compute_type: str = "int8"      # int8 = nejrychlejsi na CPU
    device: str = "cpu"
    beam_size: int = 5
    vad_filter: bool = True         # preskoci ticho, znatelne zrychli
    write_srt: bool = True


def _fmt_ts(seconds: float) -> str:
    """Format casove znacky pro SRT (00:01:23,456)."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")


class Transcriber:
    def __init__(self) -> None:
        self._model: Optional[WhisperModel] = None
        self._model_key: Optional[tuple] = None

    # ---------- nacteni modelu ----------

    def _ensure_model(self, opts: TranscribeOptions, progress: ProgressFn) -> WhisperModel:
        key = (opts.model_size, opts.device, opts.compute_type)
        if self._model is not None and self._model_key == key:
            return self._model

        progress(
            f"Nacitam model {opts.model_size} "
            f"(pri prvnim spusteni se stahuje z Hugging Face, muze trvat par minut)...",
            None,
        )
        self._model = WhisperModel(
            opts.model_size,
            device=opts.device,
            compute_type=opts.compute_type,
        )
        self._model_key = key
        progress(f"Model {opts.model_size} pripraven.", None)
        return self._model

    # ---------- vlastni prepis ----------

    def run(
        self,
        audio: Path,
        outdir: Path,
        opts: TranscribeOptions,
        progress: ProgressFn,
        cancel: threading.Event,
        on_text: Optional[Callable[[str], None]] = None,
    ) -> Path:
        """
        Prepise audio a ulozi vysledek. Vraci cestu k .txt souboru.
        Prubezne hlasi stav pres `progress` a pripadne segmenty pres `on_text`.
        """
        model = self._ensure_model(opts, progress)
        if cancel.is_set():
            raise Cancelled()

        progress("Analyzuji audio...", 0.0)
        segments, info = model.transcribe(
            str(audio),
            language=opts.language or None,
            beam_size=opts.beam_size,
            vad_filter=opts.vad_filter,
        )

        total = info.duration or 0.0
        progress(
            f"Prepisuji ({total / 60:.1f} min, jazyk: {info.language})...",
            0.0,
        )

        collected: list = []
        for seg in segments:
            if cancel.is_set():
                raise Cancelled()

            collected.append(seg)
            text = seg.text.strip()

            if on_text:
                on_text(f"[{_fmt_ts(seg.start)}] {text}")

            pct = min(100.0, (seg.end / total * 100.0) if total else 0.0)
            progress(f"Prepisuji... {seg.end / 60:.1f} / {total / 60:.1f} min", pct)

        # ---------- zapis vystupu ----------

        outdir.mkdir(parents=True, exist_ok=True)
        stem = audio.stem

        txt_path = outdir / f"{stem}.txt"
        txt_path.write_text(
            " ".join(s.text.strip() for s in collected),
            encoding="utf-8",
        )

        if opts.write_srt:
            srt_path = outdir / f"{stem}.srt"
            lines = []
            for i, s in enumerate(collected, start=1):
                lines.append(str(i))
                lines.append(f"{_fmt_ts(s.start)} --> {_fmt_ts(s.end)}")
                lines.append(s.text.strip())
                lines.append("")
            srt_path.write_text("\n".join(lines), encoding="utf-8")

        progress(f"Hotovo - {len(collected)} segmentu.", 100.0)
        return txt_path
