# Založení repozitáře

Repozitář vznikl 30. 8. 2026 z lokálního balíku `agent-kit`
jako **[Anamax443/ai-agenti](https://github.com/Anamax443/ai-agenti)** — **public**.
Veřejný schválně: je to metodická výkladní skříň, žádná citlivá data ani klíče
(ověřeno skenem před prvním commitem).

Lokální cesta na tomhle PC: `D:\git\ai-agenti`.

## Co je nastavené

**Code security**

- *Secret scanning* + *Push protection* — zapnuto. Blokuje commit s klíčem
  dřív, než se dostane do historie; vytahovat ho zpětně je horší.
- *Dependabot alerts* — zapnuto.

**CI** — `.github/workflows/kontrola.yml` běží při každém pushi:
sken tajemství (gitleaks) a kontrola odkazů v `*.md`. Testy a evaly jsou
zakomentované, dokud v repozitáři není kód agenta.

**Zvážit později** — ochrana větve `main` s povinným pull requestem.
U sólo práce zatím jen zdržuje; má smysl, až přibude druhý člověk.

## Struktura — jedno repo, nebo víc

Zatím jedno repo s metodikou a návrhy. Až se pustíš do stavby:

- **Nechat tady** jako `03-projekty/<projekt>/kod/` — přehledné, dokud jsi na tom sám
- **Odštěpit** do vlastního repa — jakmile do toho vstoupí někdo další

První varianta je výchozí. Odštěpit jde kdykoli, spojovat zpět je horší.
Pozor na duplicity: přepisovač už samostatné repo má
([mp3totxt](https://github.com/Anamax443/mp3totxt)), Gwalarn taky
([gwalarn](https://github.com/Anamax443/gwalarn)) — viz `HANDOFF.md`.
