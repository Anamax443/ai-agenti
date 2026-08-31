#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kontrola jazykovych dvojic.

Repozitar je dvojjazycny: kazdy cesky dokument ma anglicke dvojce
pojmenovane <jmeno>.en.<pripona>. Tenhle skript overi, ze:

  1. ke kazdemu ceskemu .md/.html existuje anglicke dvojce,
  2. kazde anglicke dvojce ma svuj cesky original (nezustalo po prejmenovani),
  3. zadny soubor neni v seznamu vyjimek zbytecne.

Vyjimky se zapisuji do kontrola/bez-prekladu.txt, jeden vztazny path na radek.
Seznam je zamerne rucni: co se neprekklada, ma byt videt, ne se ztratit potichu.

Spusteni:  python kontrola/dvojice.py
Navratovy kod 0 = v poradku, 1 = nalezeny nedostatky.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VYJIMKY = Path(__file__).resolve().parent / "bez-prekladu.txt"
PRIPONY = (".md", ".html")
PRESKOC_ADRESARE = {".git", ".github", "node_modules", "prepisy"}


def nacti_vyjimky() -> set[str]:
    if not VYJIMKY.exists():
        return set()
    out = set()
    for radek in VYJIMKY.read_text(encoding="utf-8").splitlines():
        radek = radek.split("#", 1)[0].strip()
        if radek:
            out.add(radek.replace("\\", "/"))
    return out


def je_anglicka(p: Path) -> bool:
    return p.name.endswith(".en" + p.suffix)


def cesky_protejsek(p: Path) -> Path:
    return p.with_name(p.name[: -len(".en" + p.suffix)] + p.suffix)


def anglicky_protejsek(p: Path) -> Path:
    return p.with_name(p.stem + ".en" + p.suffix)


def dokumenty() -> list[Path]:
    out = []
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file() or p.suffix not in PRIPONY:
            continue
        if PRESKOC_ADRESARE & set(part for part in p.relative_to(ROOT).parts):
            continue
        out.append(p)
    return out


def main() -> int:
    vyjimky = nacti_vyjimky()
    pouzite_vyjimky: set[str] = set()
    chybi_en: list[str] = []
    osirele_en: list[str] = []

    for p in dokumenty():
        rel = p.relative_to(ROOT).as_posix()

        if je_anglicka(p):
            if not cesky_protejsek(p).exists():
                osirele_en.append(rel)
            continue

        if rel in vyjimky:
            pouzite_vyjimky.add(rel)
            continue

        if not anglicky_protejsek(p).exists():
            chybi_en.append(rel)

    zbytecne = sorted(vyjimky - pouzite_vyjimky)

    if chybi_en:
        print("CHYBI ANGLICKE DVOJCE (%d):" % len(chybi_en))
        for r in chybi_en:
            print("  %s  ->  ocekavano %s" % (r, r.rsplit(".", 1)[0] + ".en." + r.rsplit(".", 1)[1]))
        print()

    if osirele_en:
        print("ANGLICKY SOUBOR BEZ CESKEHO ORIGINALU (%d):" % len(osirele_en))
        for r in osirele_en:
            print("  %s" % r)
        print()

    if zbytecne:
        print("ZBYTECNA VYJIMKA v kontrola/bez-prekladu.txt (%d):" % len(zbytecne))
        for r in zbytecne:
            print("  %s  — soubor neexistuje, nebo uz preklad ma" % r)
        print()

    if chybi_en or osirele_en or zbytecne:
        print("Kontrola dvojic NEPROSLA.")
        return 1

    prelozeno = len([p for p in dokumenty() if not je_anglicka(p)]) - len(pouzite_vyjimky)
    print("Kontrola dvojic prosla: %d dokumentu ma obe jazykove verze, "
          "%d je vedeno jako neprekladane." % (prelozeno, len(pouzite_vyjimky)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
