# AI-AGENTI

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

---

## Obsah

| Složka | Co v ní je |
|---|---|
| `00-zdroje/` | Odkud metodika pochází — citace, mapa časů v rozhovoru. |
| `01-principy/` | Obecná metodika. Platí pro libovolnou doménu. |
| `02-pripady/` | Vyplněný návrhový list — agent na příchozí faktury (HTML). |
| `03-projekty/gwalarn/` | Agent na obsah pro kapelu: scénář, moduly, zadání modulu M1. |
| `03-projekty/prepisovac/` | Desktopová aplikace na přepis audia: zadání + funkční kód. |
| `04-firemni/` | Portfolio agentů pro malou kancelář a pro velkou firmu. |
| `05-html/` | Vizuální roadmapa postupu stavby. |
| `sablony/` | Prázdný návrhový list a kostra repozitáře agenta. |

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
| Přepisovač audia | kód hotový, neotestovaný na Windows | doladit prostředí, zabalit do EXE |
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

- [HANDOFF.md](HANDOFF.md) — deník stavu (hotové / rozpracované / zbývá)
- [CONTRIBUTING.md](CONTRIBUTING.md) — konvence commitů, „prompt je kód"
- [ZALOZENI-REPO.md](ZALOZENI-REPO.md) — jak repozitář vznikl a co je nastavené
- `LICENSE` — zdroje jsou veřejně čitelné jako ukázka práce, ne open source

CI (`.github/workflows/kontrola.yml`) při každém pushi skenuje tajemství
(gitleaks) a kontroluje odkazy v `*.md`.

## Souvislosti s ostatními repozitáři

| Tady | Samostatné repo |
|---|---|
| `03-projekty/prepisovac/` | [mp3totxt](https://github.com/Anamax443/mp3totxt) — hotová CLI verze téhož |
| `03-projekty/gwalarn/` | [gwalarn](https://github.com/Anamax443/gwalarn) — web kapely |
| `02-pripady/` (faktury) | [faxx-dox](https://github.com/Anamax443/faxx-dox) — extrakce dat z dokladů |
