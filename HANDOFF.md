# HANDOFF — deník stavu: ai-agenti

Append-only. Nejnovější záznam nahoru. Slouží k pokračování z jiného počítače / po pauze.

## 2026-08-30 — doplněn zdroj metodiky
- **Hotové:** `00-zdroje/ZDROJE.md` — citace pořadu (Keci a politika, speciál
  s Markem Bartošem „Umělá inteligence je naše UFO"), parametry přepisu
  (mp3totxt 0.1.0, model `medium`, 55:51 audia, poměr 1,81×) a mapa
  19 časů → kapitoly v `01-principy/`. Ověřeno proti `.json` přepisu.
- **Vědomé rozhodnutí:** přepis (`.txt`/`.json`/`.srt`/`.vtt`) leží
  v `00-zdroje/prepisy/` jen lokálně a je v `.gitignore`. Repo je veřejné
  a přepis cizího pořadu s placenou druhou polovinou do něj nepatří.
  MP3 se nekopírovalo vůbec.
- **Zbývá:** stejný postup u dalších zdrojů (přepis mimo git, sem citace a časy).

## 2026-08-30 — založení repozitáře
- **Hotové:** repo `Anamax443/ai-agenti` (public) založeno z lokálního balíku
  `agent-kit`. Obsah: metodika (`01-principy/`), vyplněný případ (`02-pripady/`),
  rozpracované projekty (`03-projekty/`), firemní portfolia (`04-firemni/`),
  vizuální postup (`05-html/`), šablony (`sablony/`).
  Doplněno podle project-standard: `LICENSE`, `.editorconfig`, `.gitattributes`,
  tenhle deník. CI `kontrola.yml` (gitleaks + kontrola odkazů) běží od prvního pushe.
  V Code security zapnuto secret scanning + push protection + Dependabot.
- **Rozpracované:** —
- **Zbývá / otevřené otázky:**
  - `03-projekty/prepisovac/kod/` je starší varianta téhož, co už žije
    v samostatném repu `Anamax443/mp3totxt` (funkční CLI + testy).
    Rozhodnout: nechat tady jen `ZADANI-prepisovac.md` jako návrhový artefakt
    a kód smazat s odkazem na mp3totxt, nebo naopak.
  - Gwalarn: návrh agenta na obsah sedí k repu `Anamax443/gwalarn`.
    Rozhodnout, jestli se `03-projekty/gwalarn/` odštěpí tam.
  - Vybrat prvního agenta z `04-firemni/AGENTI-mala-kancelar.md` a postavit ho.
