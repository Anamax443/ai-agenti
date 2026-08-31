# HANDOFF — deník stavu: ai-agenti

Append-only. Nejnovější záznam nahoru. Slouží k pokračování z jiného počítače / po pauze.

## 2026-08-31 — vizuální výstupy, dvojjazyčnost, kontrola dvojic

- **Hotové — čtyři nové stránky v `05-html/`,** česky i anglicky, ve stejném vizuálním
  jazyce jako `postup-stavby.html` (stejná paleta i písmo, aby to drželo jednu řeč):
  - [`manazerske-shrnuti.html`](05-html/manazerske-shrnuti.html) — **jedna A4 na výšku
    k vytištění pro vedení.** Jádro, dva konce procesu s výslovně odstraněným třetím,
    co to znamená provozně (náklady, odpovědnost, identita, dohled, regulace),
    devět fází s vyznačenými třemi nepřeskočitelnými, důkaz z auditu JobWatch a tři čísla.
    `@page A4 portrait`, ověřeno, že se to na jednu stranu vejde.
  - [`mapa-mysleni.html`](05-html/mapa-mysleni.html) — myšlenková mapa: jádro uprostřed,
    pět větví (základ, stavba, kontakt s okolím, kontrola, provoz), pod nimi antivzory
    a vstupní bod. Levá strana odpovídá „z čeho to je", pravá „jak se to provozuje".
  - [`tok-informaci.html`](05-html/tok-informaci.html) — tok informací agentem: u každého
    úseku je vidět, co vstupuje a co vychází, kdo krok dělá (model / kód / člověk),
    a kde leží **hranice důvěry**, za kterou je cizí text jen data. Na konci tři reálné
    vady z auditu namapované na úseky trasy.
  - [`vyvojovy-diagram.html`](05-html/vyvojovy-diagram.html) — vývojový diagram F0–F8 v SVG:
    fáze → brána → podmínky → další fáze, s čárkovanou větví „ne" zpět na tutéž fázi.
    Souřadnice jsou na pravidelné mřížce, takže jde editovat ručně.
- **Repozitář je nově dvojjazyčný.** Konvence `<jméno>.en.md` / `<jméno>.en.html`,
  při rozporu platí česká verze. Přeloženo jádro: principy, build předpis, návrhový list,
  zdroje, audit job-watch, kostra agenta, README, AGENTS, CONTRIBUTING, ZALOZENI-REPO,
  STATUS, portfolia v `04-firemni/`.
- **Nová funkce nese vlastní kontrolu:** [`kontrola/dvojice.py`](kontrola/dvojice.py) ověří,
  že ke každému českému dokumentu existuje anglické dvojče a naopak. Výjimky se zapisují
  ručně do `kontrola/bez-prekladu.txt` — chybějící překlad má být vidět, ne tiše zmizet.
  Zapojeno do CI vedle gitleaks a lychee. Skript zároveň hlásí *zbytečnou* výjimku,
  takže se seznam sám uklidí, až soubor zmizí.
- **Rozpracované:** —
- **Zbývá:**
  - Dopřeložit `03-projekty/` (gwalarn, zadání přepisovače) a
    `02-pripady/navrhovy-list-faktury.html`, `05-html/postup-stavby.html`.
    Kontrola dvojic je vypisuje jmenovitě.
  - **Smazání `03-projekty/prepisovac/kod/` pořád visí na oprávnění.** Rozhodnutí platí
    (viz záznam níž), příkaz je `git rm -r 03-projekty/prepisovac/kod`.
  - Beze změny: UX kapitola z Albady, Vorel a Lanham, slovník k veřejným předpisům,
    gwalarn, první agent z `04-firemni/`.

## 2026-08-31 — AGENTS.md
- **Hotové:** [`AGENTS.md`](AGENTS.md) — pravidla pro AI asistenty pracující v repu.
  Podstatné je první z nich: **kód sem nepatří**. Když z návrhu vznikne funkční věc,
  založí se jí vlastní repo a odsud vede odkaz; rozpracovaný kód, který tu zůstane
  ležet, se rozejde s tím, co běží, a nikdo nepozná, která kopie je pravda. Dál:
  česky s diakritikou, odkaž nekopíruj, přepisy cizích zdrojů do veřejného repa
  nikdy, `HANDOFF.md` a `STATUS.html` držet v souladu, návrhový list před prvním
  řádkem kódu, nepřeskočitelné F1/F3/F6. Zmíněno v `README.md` (Standard projektu)
  a v `STATUS.html` (obsah repa + hotové).
- **Rozpracované:** —
- **Zbývá:**
  - **Duplicita přepisovače** — rozhodnuto smazat `03-projekty/prepisovac/kod/`
    a nechat tu jen `ZADANI-prepisovac.md` jako návrhový artefakt s ukazatelem na
    [mp3totxt](https://github.com/Anamax443/mp3totxt). Důvod není jen „dvě kopie":
    ten prototyp **neprošel vlastní bránou**. Zadání označuje `preflight.py` za
    klíčový modul a „nic se nesmí spustit naslepo" za klíčový požadavek — v kódu
    žádný `preflight.py`, `validators.py` ani `appstate.py` není a testy taky ne.
    Zbyl GUI prototyp ze tří souborů s jedinou kontrolou `audio.exists()`.
    Co `mp3totxt` oproti zadání **nepokrývá**: GUI, stahování z URL přes yt-dlp
    a preflight. Ta mezera se smazáním kódu neztratí — je popsaná v zadání.
    *Samotné smazání zatím neproběhlo, blokuje ho oprávnění.*
  - `AGENTS.md` do ostatních repozitářů.
  - Beze změny: UX kapitola z Albady, Vorel a Lanham, slovník k veřejným předpisům,
    gwalarn, první agent z `04-firemni/`.

## 2026-08-30 — první ostré použití předpisu + stavový list
- **Hotové:** předpis pustěn na [`Anamax443/job-watch`](https://github.com/Anamax443/job-watch),
  jediného agenta, který běží naostro. Našel **tři vady, které testy nenašly**: vypínač,
  který uzavře záznam běhu, ale pipeline nezastaví; pád běhu, o kterém se nikdo nedozví,
  protože notifikace se posílají jen na nálezy; a text inzerátu od cizích lidí jdoucí do
  modelu bez obalu. Rozbor v [`02-pripady/AUDIT-job-watch.md`](02-pripady/AUDIT-job-watch.md),
  záznam nálezu a diagram běhu v repu projektu.
- **Co to říká o předpisu:** nálezy padly do F4 a F6 — tedy do fází doplněných naposled
  (z Albady a rozboru zdrojů). Fáze, které v metodice byly od začátku — determinismus,
  limity, identita — obstály. Slabý, ale reálný důkaz, že se doplňovalo správným směrem.
- **Přidán `STATUS.html`** — stavový list podle „klasiky": přehled, obsah repa, fáze F0–F8
  s branami, zdroje metodiky, hotové vs. zbývá. Vizuálně sjednocený se `STATUS.html`
  v job-watch, ať to drží jednu řeč napříč projekty.
- **Zbývá:** kapitola o UX agenta (z Albady zatím nevyužitá), Vorel a Lanham,
  slovník k veřejným předpisům, `AGENTS.md`.

## 2026-08-30 — rozbor Albady, doplnění předpisu
- **Hotové:** přečten celý text Albada, *Building Applications with AI Agents*
  (O'Reilly 2025, 355 s.). Do `sablony/BUILD-PREDPIS.md` doplněno sedm věcí,
  které nám chyběly: discoverability textového rozhraní (F0), vypínání nástrojů
  konfigurací (F2), měřicí metriky tool recall/precision + parameter accuracy (F4),
  rozpočet na eskalace ~10 %, princip nejmenší moci a růst autonomie (F5),
  čtyři způsoby selhání lidského dohledu (F6), pravidlo chyba-vs-rozptyl
  a běh naslepo (F7), PSI na posun rozdělení a zlaté cesty (F8).
- **Šablona evalů** přepsána: očekávaný koncový stav místo očekávaného textu,
  tabulka metrik, návod na výrobu okrajových případů, ukázka s útokem.
- **Návrhový list:** odkaz na tréninkové CTF na prompt injection.
- **Citace knihy** v `00-zdroje/ZDROJE.md` včetně mapy kapitola → co jsme převzali.
  Text knihy v repu není (warez balík, viz pravidlo u přepisů).
- **Zbývá:** projít Vorla (NoOps) a Lanhama; z Albady nevyužito UX kapitola
  jako celek a kapitoly o multiagentní koordinaci a fine-tuningu (mimo náš záběr).

## 2026-08-30 — build předpis a úprava šablon
- **Hotové:** `sablony/BUILD-PREDPIS.md` — obecný fázový postup F0–F8, každá
  fáze s bránou. Doplňuje mezeru mezi návrhovým listem (co navrhnout)
  a `05-html/postup-stavby.html` (konkrétní plán jednoho projektu).
  Nepřeskočitelné minimum: F1 reálný vzorek, F3 dva konce procesu, F6 vypínač.
- **Návrhový list** rozšířen o dvě sekce: *Nepřátelský vstup* (prompt injection
  u agentů, co čtou cizí texty) a *Regulace a data* (AI Act, osobní údaje, retence).
- **Odstraněna duplicita:** `sablony/kostra-agenta/NAVRH.md` byl bajt po bajtu
  kopií návrhového listu. Teď je z něj ukazatel na jediný zdroj pravdy —
  dvě kopie by se rozešly a nikdo by si nevšiml které.
- **Zbývá:** porovnat předpis s veřejnými (12-factor agents, Anthropic
  workflows-vs-agents) a doplnit, co z nich dává smysl převzít.

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
