#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inventář bran a generátor měřicího protokolu.

Proč to existuje
----------------
Předpis má 45 podmínek v devíti branách. Dokud se jejich počet psal ručně, rozešel se:
podklad pro oponenturu uváděl postupně 38, 37, 41 a 42 na čtyřech různých místech, a nikdo
si toho nevšiml, dokud to nenašla externí recenze. **Ručně psaný počet opakovaný ve třech
souhrnech se rozejde vždycky.**

Řešení je nejlevnější možné: žádný druhý seznam. Zdrojem pravdy je `sablony/BUILD-PREDPIS.md`
a všechno ostatní se z něj odvozuje — počet, inventář i prázdný měřicí protokol.

Co kontroluje
-------------
1. Česká a anglická verze mají **stejný počet podmínek v každé bráně**. Půlka přeložené
   brány je stejná vada jako chybějící překlad, jen se hůř hledá.
2. Každá fáze F0–F8 má aspoň jednu podmínku.

Použití
-------
    python kontrola/brany.py                     kontrola (CI)
    python kontrola/brany.py --seznam            inventář s identifikátory
    python kontrola/brany.py --protokol v0.9     prázdný měřicí protokol na stdout

Identifikátory
--------------
`F3.4` = čtvrtá podmínka brány F3. Jsou **poziční**, ne trvalé: co je F3.4 dnes, může být
F3.5 po vložení nové podmínky. To není vada — měření se vždycky odkazuje na **vydání
etalonu** (`ai-agenti v0.9`), a to jeho význam pevně určuje. Tak to dělají i normy:
`ISO 27001:2013 A.9.2.3` znamená něco jiného než tentýž kód ve vydání 2022.
"""
import io
import os
import re
import sys

KOREN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CS = os.path.join("sablony", "BUILD-PREDPIS.md")
EN = os.path.join("sablony", "BUILD-PREDPIS.en.md")

FAZE = re.compile(r"^## (F\d)\s+—\s+(.+?)\s*$")
PODMINKA = re.compile(r"^- \[ \] (.*)$")
POKRACOVANI = re.compile(r"^ {6}(\S.*)$")


def nacti(rel):
    """Vytáhne z předpisu fáze a jejich podmínky v pořadí, v jakém stojí v textu."""
    with io.open(os.path.join(KOREN, rel), encoding="utf-8") as f:
        radky = f.read().splitlines()

    faze = []           # [(kod, nazev, [text podminky, ...])]
    aktualni = None
    for r in radky:
        m = FAZE.match(r)
        if m:
            aktualni = (m.group(1), m.group(2), [])
            faze.append(aktualni)
            continue
        if aktualni is None:
            continue
        m = PODMINKA.match(r)
        if m:
            aktualni[2].append(m.group(1).strip())
            continue
        # Odsazené pokračování patří k předchozí podmínce, ne k nové.
        m = POKRACOVANI.match(r)
        if m and aktualni[2]:
            aktualni[2][-1] += " " + m.group(1).strip()
    return faze


def kontrola():
    cs, en = nacti(CS), nacti(EN)
    chyby = []

    kody_cs = [k for k, _, _ in cs]
    kody_en = [k for k, _, _ in en]
    if kody_cs != kody_en:
        chyby.append("fáze se neshodují: CS %s vs EN %s" % (kody_cs, kody_en))

    for (kod, nazev, pod_cs), (_, _, pod_en) in zip(cs, en):
        if not pod_cs:
            chyby.append("%s (%s) nemá žádnou podmínku" % (kod, nazev))
        if len(pod_cs) != len(pod_en):
            chyby.append(
                "%s: CS má %d podmínek, EN %d — půlka přeložené brány je vada"
                % (kod, len(pod_cs), len(pod_en))
            )

    celkem = sum(len(p) for _, _, p in cs)
    if chyby:
        print("Kontrola bran NEPROSLA:")
        for ch in chyby:
            print("  - " + ch)
        return 1

    rozpis = " · ".join("%s %d" % (k, len(p)) for k, _, p in cs)
    print("Kontrola bran prosla: %d podminek, CS i EN se shoduji." % celkem)
    print("  " + rozpis)
    return 0


def seznam():
    for kod, nazev, podminky in nacti(CS):
        print("\n%s — %s" % (kod, nazev))
        for i, t in enumerate(podminky, 1):
            print("  %s.%-2d %s" % (kod, i, t))
    return 0


def protokol(verze):
    cs = nacti(CS)
    celkem = sum(len(p) for _, _, p in cs)
    out = []
    a = out.append

    a("# MĚŘENÍ — <název předmětu>")
    a("")
    a("| | |")
    a("|---|---|")
    a("| **Etalon** | `ai-agenti %s` |" % verze)
    a("| **Předmět** | `<repozitář>` @ `<commit>` |")
    a("| **Měřič** | <kdo — a jestli je totožný s autorem předmětu> |")
    a("| **Datum** | <kdy> |")
    a("| **Přísnost** | N / Z / V *(osa systému, principy §7)* |")
    a("| **Podmínek** | %d |" % celkem)
    a("")
    a("**Výsledek:** `ano` splněno · `ne` nesplněno · `nelze` nelze na tomto agentovi měřit")
    a("")
    a("**Stupeň:** `U0` tvrzeno · `U1` v kódu · `U2` kryto testem · `U3` vyvoláno")
    a("v prostředí · `U4` nezávisle uzavřeno")
    a("")
    a("> **`nelze` je plnohodnotný výsledek.** Bez něj se měřič tlačí do ano/ne i tam, kde")
    a("> brána na daného agenta nesedí — a přesně tak vznikl spor o bránu F4 u agenta,")
    a("> jehož backend existuje jen za běhu. U `nelze` je poznámka povinná.")
    a("")
    a("> **U `ano` je povinný důkaz.** Příkaz sám není důkaz; důkazem je jeho výstup,")
    a("> soubor, nebo test. Bez důkazu platí nejvýš `U0`.")
    a("")
    a("## Souhrn *(vyplň až nakonec)*")
    a("")
    a("| | počet |")
    a("|---|---|")
    a("| ano | |")
    a("| ne | |")
    a("| nelze | |")
    a("| z toho na stupni U2 a výš | |")
    a("")
    a("**Nálezy, které měření nenašlo** *(doplň, až se nějaké objeví jinudy — tenhle řádek")
    a("je kalibrace etalonu, ne ostuda měřiče):*")
    a("")

    for kod, nazev, podminky in cs:
        a("---")
        a("")
        a("## %s — %s" % (kod, nazev))
        a("")
        a("| ID | Podmínka | Výsledek | Stupeň | Důkaz / poznámka |")
        a("|---|---|---|---|---|")
        for i, t in enumerate(podminky, 1):
            t = t.replace("|", "\\|")
            a("| **%s.%d** | %s | | | |" % (kod, i, t))
        a("")

    print("\n".join(out))
    return 0


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    if arg == "--seznam":
        return seznam()
    if arg == "--protokol":
        return protokol(sys.argv[2] if len(sys.argv) > 2 else "<verze>")
    if arg:
        print(__doc__)
        return 2
    return kontrola()


if __name__ == "__main__":
    sys.exit(main())
