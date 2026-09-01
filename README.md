# AI-AGENTI

**Čeština** · [English](README.en.md)

Metodika stavby AI agentů a rozpracované projekty.

Vzniklo z rozboru rozhovoru s Markem Bartošem (podcast Keci a politika,
„Umělá inteligence je naše UFO") a z návrhové práce na vlastních projektech.
Doplněno o doporučení Anthropic a OpenAI ke stavbě agentů.

---

## Kde začít

Přečti si **[01-principy/PRINCIPY-stavby-agentu.md](01-principy/PRINCIPY-stavby-agentu.md)**.
Zbytek jsou aplikace téhož na konkrétní případy.

Když potřebuješ navrhnout nového agenta, vezmi
**[sablony/navrhovy-list.md](sablony/navrhovy-list.md)** a vyplň ho dřív,
než napíšeš první řádek kódu.

Když ho pak stavíš, drž se **[sablony/BUILD-PREDPIS.md](sablony/BUILD-PREDPIS.md)** —
fáze F0–F8, každá s bránou, kterou musíš projít, než začne další.

Jak předpis dopadl v ostrém provozu, ukazuje
**[02-pripady/AUDIT-job-watch.md](02-pripady/AUDIT-job-watch.md)** — na běžícím agentovi
našel čtyři vady, které testy nenašly — a všechny jsou k 1. 9. 2026 opravené.

### Když to potřebuješ ukázat někomu jinému

| Výstup | K čemu |
|---|---|
| [Manažerské shrnutí](05-html/manazerske-shrnuti.html) | jedna A4 na výšku, k vytištění pro vedení |
| [Myšlenková mapa](05-html/mapa-mysleni.html) | celá metodika na jedné ploše, od jádra ven |
| [Tok informací](05-html/tok-informaci.html) | kudy data jdou, kdo je zpracovává, kde je hranice důvěry |
| [Vývojový diagram](05-html/vyvojovy-diagram.html) | fáze F0–F8 s branami a návraty |

Každá stránka má anglickou verzi (`*.en.html`) a přepínač jazyka v hlavičce.
Manažerské shrnutí a vývojový diagram jsou nastavené na tisk A4.

---

## Obsah

| Složka | Co v ní je |
|---|---|
| `00-zdroje/` | Odkud metodika pochází — citace, mapa časů v rozhovoru. |
| `01-principy/` | Obecná metodika. Platí pro libovolnou doménu. |
| `02-pripady/` | Vyplněný návrhový list (faktury) a **audit běžícího agenta** proti předpisu. |
| `03-projekty/gwalarn/` | Agent na obsah pro kapelu: scénář, moduly, zadání modulu M1. |
| `03-projekty/prepisovac/` | Zadání desktopové aplikace na přepis audia. Podsložka `kod/` je rozhodnutá ke smazání — nedodělaný prototyp vedle hotového [mp3totxt](https://github.com/Anamax443/mp3totxt), viz `HANDOFF.md`. |
| `04-firemni/` | Portfolio agentů pro malou kancelář a pro velkou firmu. |
| `05-html/` | Vizuální výstupy: manažerské shrnutí, myšlenková mapa, tok informací, vývojový diagram, roadmapa. |
| `sablony/` | **Build předpis** (fáze a brány), prázdný návrhový list a kostra repozitáře agenta. |
| `kontrola/` | Kontrola jazykových dvojic — běží v CI. |

---

## Jádro v jedné větě

> **AI rozpoznává. Kód vykonává.**

Model dostává tři typy úloh — rozpoznání záměru, extrakci struktury,
syntézu textu. Všechno ostatní je deterministický kód. Tím vzniká
systém, který má jen dva možné konce: selže s hlášením, nebo dopadne dobře.
Třetí větev, kdy udělá něco, co nikdo nechtěl, je odstraněná návrhem.

---

## Stav projektů

| Projekt | Stav | Další krok |
|---|---|---|
| Přepisovač audia | zadání hotové; přepis samotný řeší [mp3totxt](https://github.com/Anamax443/mp3totxt) | rozhodnout o GUI a stahování z URL — to `mp3totxt` nepokrývá |
| Gwalarn — agent na obsah | návrh hotový | modul M1 (ffmpeg), účty u Mety |
| Agenti pro kancelář | návrh | vybrat prvního a postavit |

---

## Poznámky ke zdrojům

Podcast byl přepsán lokálně přes [mp3totxt](https://github.com/Anamax443/mp3totxt)
(faster-whisper, model `medium`). Přepis komolí vlastní jména a pokrývá
jen první polovinu pořadu — druhá je za předplatným. Samotný přepis
v repozitáři není, drží se lokálně mimo git.

Citace, metoda přepisu a mapa „co zaznělo v kterém čase → kam se to
v metodice promítlo" jsou v **[00-zdroje/ZDROJE.md](00-zdroje/ZDROJE.md)**.

Odkazy na regulaci (AI Act) odpovídají stavu k srpnu 2026, po vstupu
Digital Omnibus v platnost 27. července 2026. Termíny se mění, ověřuj.

---

## Standard projektu

Repozitář drží [project-standard](https://github.com/Anamax443/project-standard):

- [STATUS.html](STATUS.html) — stavový list ke čtení v prohlížeči (přehled, fáze, zdroje)
- [HANDOFF.md](HANDOFF.md) — deník stavu (hotové / rozpracované / zbývá)
- [CONTRIBUTING.md](CONTRIBUTING.md) — konvence commitů, „prompt je kód"
- [AGENTS.md](AGENTS.md) — pravidla pro AI asistenty pracující v repu (kód sem nepatří, odkaž nekopíruj)
- [ZALOZENI-REPO.md](ZALOZENI-REPO.md) — jak repozitář vznikl a co je nastavené
- `LICENSE` — zdroje jsou veřejně čitelné jako ukázka práce, ne open source

CI (`.github/workflows/kontrola.yml`) při každém pushi skenuje tajemství
(gitleaks), kontroluje odkazy v `*.md` a ověřuje jazykové dvojice
(`kontrola/dvojice.py`).

## Jazyk

Repozitář je dvojjazyčný. Každý dokument má anglické dvojče `<jméno>.en.md`
(u stránek `.en.html`). Když si obě verze odporují, platí česká — angličtina
je překlad, ne odnož. Co se vědomě nepřekládá, je vypsané
v [kontrola/bez-prekladu.txt](kontrola/bez-prekladu.txt), aby to bylo vidět
a nechybělo to potichu.

## Souvislosti s ostatními repozitáři

| Tady | Samostatné repo |
|---|---|
| `03-projekty/prepisovac/` | [mp3totxt](https://github.com/Anamax443/mp3totxt) — hotové CLI; nepokrývá GUI ani stahování z URL |
| `03-projekty/gwalarn/` | [gwalarn](https://github.com/Anamax443/gwalarn) — web kapely |
| `02-pripady/` (faktury) | [faxx-dox](https://github.com/Anamax443/faxx-dox) — extrakce dat z dokladů |
