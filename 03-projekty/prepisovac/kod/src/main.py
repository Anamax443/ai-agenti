"""
Prepisovac audia - GUI.

Vstup:  URL (YouTube, podcast) nebo lokalni audio/video soubor
Vystup: .txt (+ .srt) ve zvolene slozce

Vsechna tezka prace bezi ve vlakne na pozadi, GUI komunikuje
pres frontu - okno tedy nikdy nezamrzne a jde prerusit.
"""

from __future__ import annotations

import os
import queue
import subprocess
import sys
import threading
import traceback
from pathlib import Path

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

sys.path.insert(0, str(Path(__file__).parent))

from downloader import download_audio, is_url  # noqa: E402
from transcriber import Cancelled, TranscribeOptions, Transcriber  # noqa: E402

MODELS = ["tiny", "base", "small", "medium", "large-v3-turbo", "large-v3"]
LANGS = [("cestina", "cs"), ("anglictina", "en"), ("autodetekce", "")]


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Prepisovac audia")
        self.geometry("820x560")
        self.minsize(640, 460)

        self.q: queue.Queue = queue.Queue()
        self.cancel = threading.Event()
        self.transcriber = Transcriber()
        self.worker: threading.Thread | None = None
        self.last_output: Path | None = None

        self._build_ui()
        self.after(100, self._pump)

    # ---------- rozvrzeni ----------

    def _build_ui(self) -> None:
        pad = {"padx": 8, "pady": 4}

        top = ttk.Frame(self)
        top.pack(fill="x", **pad)
        top.columnconfigure(1, weight=1)

        ttk.Label(top, text="Zdroj:").grid(row=0, column=0, sticky="w")
        self.source_var = tk.StringVar()
        ttk.Entry(top, textvariable=self.source_var).grid(row=0, column=1, sticky="ew", padx=4)
        ttk.Button(top, text="Soubor...", command=self._pick_file).grid(row=0, column=2)

        ttk.Label(top, text="Vystup:").grid(row=1, column=0, sticky="w")
        self.outdir_var = tk.StringVar(value=str(Path.home() / "Downloads"))
        ttk.Entry(top, textvariable=self.outdir_var).grid(row=1, column=1, sticky="ew", padx=4)
        ttk.Button(top, text="Slozka...", command=self._pick_dir).grid(row=1, column=2)

        # --- volby ---
        opts = ttk.LabelFrame(self, text="Nastaveni")
        opts.pack(fill="x", **pad)

        ttk.Label(opts, text="Model:").grid(row=0, column=0, sticky="w", padx=6, pady=6)
        self.model_var = tk.StringVar(value="medium")
        ttk.Combobox(
            opts, textvariable=self.model_var, values=MODELS, width=16, state="readonly"
        ).grid(row=0, column=1, padx=4)

        ttk.Label(opts, text="Jazyk:").grid(row=0, column=2, sticky="w", padx=6)
        self.lang_var = tk.StringVar(value="cestina")
        ttk.Combobox(
            opts,
            textvariable=self.lang_var,
            values=[n for n, _ in LANGS],
            width=14,
            state="readonly",
        ).grid(row=0, column=3, padx=4)

        self.srt_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(opts, text="Ulozit i .srt", variable=self.srt_var).grid(
            row=0, column=4, padx=12
        )

        # --- tlacitka ---
        btns = ttk.Frame(self)
        btns.pack(fill="x", **pad)
        self.start_btn = ttk.Button(btns, text="Spustit prepis", command=self._start)
        self.start_btn.pack(side="left")
        self.cancel_btn = ttk.Button(btns, text="Prerusit", command=self._cancel, state="disabled")
        self.cancel_btn.pack(side="left", padx=6)
        self.open_btn = ttk.Button(
            btns, text="Otevrit vysledek", command=self._open_result, state="disabled"
        )
        self.open_btn.pack(side="left")

        # --- prubeh ---
        self.progress = ttk.Progressbar(self, mode="determinate", maximum=100)
        self.progress.pack(fill="x", padx=8, pady=(8, 2))

        self.log = tk.Text(self, wrap="word", height=16, font=("Consolas", 9))
        self.log.pack(fill="both", expand=True, padx=8, pady=4)
        sb = ttk.Scrollbar(self.log, command=self.log.yview)
        sb.pack(side="right", fill="y")
        self.log.configure(yscrollcommand=sb.set)

        # --- stavovy radek ---
        self.status_var = tk.StringVar(value="Pripraveno.")
        ttk.Label(
            self, textvariable=self.status_var, relief="sunken", anchor="w", padding=(6, 3)
        ).pack(fill="x", side="bottom")

    # ---------- obsluha ----------

    def _pick_file(self) -> None:
        path = filedialog.askopenfilename(
            title="Vyber audio nebo video",
            filetypes=[
                ("Audio a video", "*.mp3 *.m4a *.wav *.ogg *.opus *.flac *.mp4 *.mkv *.webm"),
                ("Vsechny soubory", "*.*"),
            ],
        )
        if path:
            self.source_var.set(path)

    def _pick_dir(self) -> None:
        path = filedialog.askdirectory(title="Kam ulozit vysledek")
        if path:
            self.outdir_var.set(path)

    def _lang_code(self) -> str:
        return dict(LANGS).get(self.lang_var.get(), "cs")

    def _start(self) -> None:
        source = self.source_var.get().strip()
        if not source:
            messagebox.showwarning("Chybi zdroj", "Zadej URL nebo vyber soubor.")
            return

        outdir = Path(self.outdir_var.get().strip() or Path.home() / "Downloads")

        opts = TranscribeOptions(
            model_size=self.model_var.get(),
            language=self._lang_code(),
            write_srt=self.srt_var.get(),
        )

        self.cancel.clear()
        self.log.delete("1.0", "end")
        self.progress["value"] = 0
        self.start_btn.configure(state="disabled")
        self.cancel_btn.configure(state="normal")
        self.open_btn.configure(state="disabled")

        self.worker = threading.Thread(
            target=self._run, args=(source, outdir, opts), daemon=True
        )
        self.worker.start()

    def _cancel(self) -> None:
        self.cancel.set()
        self.status_var.set("Prerusuji...")

    def _open_result(self) -> None:
        if not self.last_output:
            return
        if sys.platform == "win32":
            os.startfile(self.last_output)  # noqa: S606
        else:
            subprocess.run(["xdg-open", str(self.last_output)], check=False)

    # ---------- vlakno na pozadi ----------

    def _run(self, source: str, outdir: Path, opts: TranscribeOptions) -> None:
        def progress(msg: str, pct: float | None = None) -> None:
            self.q.put(("status", msg))
            if pct is not None:
                self.q.put(("progress", pct))

        try:
            if is_url(source):
                audio = download_audio(source, outdir, progress, self.cancel)
            else:
                audio = Path(source)
                if not audio.exists():
                    raise FileNotFoundError(f"Soubor neexistuje: {audio}")

            txt = self.transcriber.run(
                audio,
                outdir,
                opts,
                progress,
                self.cancel,
                on_text=lambda line: self.q.put(("log", line)),
            )
            self.q.put(("done", txt))

        except Cancelled:
            self.q.put(("cancelled", None))
        except Exception as exc:  # noqa: BLE001
            self.q.put(("error", f"{exc}\n\n{traceback.format_exc()}"))

    # ---------- prenos zprav do GUI ----------

    def _pump(self) -> None:
        try:
            while True:
                kind, payload = self.q.get_nowait()

                if kind == "status":
                    self.status_var.set(payload)
                elif kind == "progress":
                    self.progress["value"] = payload
                elif kind == "log":
                    self.log.insert("end", payload + "\n")
                    self.log.see("end")
                elif kind == "done":
                    self.last_output = payload
                    self.status_var.set(f"Hotovo: {payload}")
                    self.progress["value"] = 100
                    self._idle()
                    self.open_btn.configure(state="normal")
                elif kind == "cancelled":
                    self.status_var.set("Preruseno uzivatelem.")
                    self._idle()
                elif kind == "error":
                    self.status_var.set("Chyba - detail v logu.")
                    self.log.insert("end", "\n=== CHYBA ===\n" + str(payload) + "\n")
                    self.log.see("end")
                    self._idle()

        except queue.Empty:
            pass

        self.after(100, self._pump)

    def _idle(self) -> None:
        self.start_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled")


if __name__ == "__main__":
    App().mainloop()
