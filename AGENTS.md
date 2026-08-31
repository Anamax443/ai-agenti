# AGENTS.md — jak v tomhle repozitáři pracovat

Pokyny pro AI asistenty (Claude Code, Codex, Copilot a spol.). Pro lidi platí totéž,
jen si to přečtou dobrovolně. Konvence commitů a checklisty jsou
v [CONTRIBUTING.md](CONTRIBUTING.md) — tady je to, co z nich agent sám neuhodne.

---

## Co tenhle repozitář je

**Předpis, ne aplikace.** Neobsahuje kód agenta, nemá build ani jednotkové testy.
Obsahuje metodiku (`01-principy/`), fázový postup s branami (`sablony/BUILD-PREDPIS.md`),
prázdné šablony k vyplnění (`sablony/`) a vyplněné případy (`02-pripady/`).

Z toho plyne první pravidlo: **kód sem nepatří.** Když z návrhu vznikne funkční věc,
založí se jí vlastní repozitář a odsud na něj vede odkaz. Rozpracovaný kód, který tu
zůstane ležet, se rozejde s tím, co běží — a nikdo si nevšimne, která kopie je pravda.
Stejné pravidlo platí pro text: `sablony/kostra-agenta/NAVRH.md` byl bajt po bajtu
kopií návrhového listu a je z něj dnes jen ukazatel. **Odkaž, nekopíruj.**

## Jazyk a forma

- Píše se **česky**, včetně diakritiky. Názvy souborů, cesty a kód bez diakritiky.
- Věcně, bez marketingu. Tvrzení bez důvodu do textu nepatří.
- Jde-li o výčet, je tabulka lepší než odstavec.

## Kde je pravda

| Téma | Soubor |
|---|---|
| Obecná metodika, 16 kapitol | [01-principy/PRINCIPY-stavby-agentu.md](01-principy/PRINCIPY-stavby-agentu.md) |
| Co vyplnit před stavbou | [sablony/navrhovy-list.md](sablony/navrhovy-list.md) |
| Jak stavět — fáze F0–F8 a brány | [sablony/BUILD-PREDPIS.md](sablony/BUILD-PREDPIS.md) |
| Jak předpis dopadl naostro | [02-pripady/AUDIT-job-watch.md](02-pripady/AUDIT-job-watch.md) |
| Stav a deník | [HANDOFF.md](HANDOFF.md) + vizuální dvojče `STATUS.html` |

## Co hlídá CI

`.github/workflows/kontrola.yml` běží na každý push:

- **gitleaks** — sken tajemství v celé historii.
- **lychee** `--offline` nad `**/*.md` — každý relativní odkaz musí ukazovat na
  existující soubor. Když soubor přejmenuješ nebo smažeš, oprav odkazy na něj,
  jinak CI spadne. Externí URL se offline nekontrolují, takže překlep v adrese
  na GitHub CI nechytí — ověř ho ručně.

Kroky `testy` a `evaly` jsou ve workflow zakomentované. Odkomentují se, až tu bude
kód agenta — což podle pravidla výš nemá nastat.

## Co sem nesmí

- **Přepisy a plné texty cizích zdrojů.** Repo je veřejné. `00-zdroje/prepisy/`
  je v `.gitignore` a zůstane tam. Do repa jde citace, parametry přepisu a mapa
  „co zaznělo v kterém čase → kam se to v metodice promítlo". Nic víc.
- **Tajemství jakéhokoli druhu.** Ani v ukázkách — použij zjevný zástupný text.

## Deník

`HANDOFF.md` je append-only, **nejnovější záznam nahoru**, členění
*Hotové / Rozpracované / Zbývá*. Měníš-li obsah repa, zapiš to tam a stejnou změnu
promítni do `STATUS.html` — ty dva si nesmějí odporovat. Když jeden z nich upravíš
a druhý ne, příště nikdo neví, který lže.

## Než navrhneš agenta

Pořadí není doporučení, je to předpis:

1. **`sablony/navrhovy-list.md` vyplněný dřív** než vznikne první řádek kódu.
2. **F1** — jádro ověřené na reálném vzorku, ne na vymyšleném.
3. **F3** — deterministická páteř se dvěma konci (selže s hlášením / dopadne dobře),
   ještě bez modelu.
4. **F6** — vypínač, který běh opravdu zastaví.

Tyhle čtyři se nepřeskakují. Zbylé fáze a jejich brány jsou
v [sablony/BUILD-PREDPIS.md](sablony/BUILD-PREDPIS.md); u malého agenta jde část
z nich zjednodušit — kapitola *Co u malého agenta přeskočit* říká, co konkrétně.
Brána není formalita: je to seznam podmínek, bez kterých další fáze stojí na písku.

## Jádro v jedné větě

> **AI rozpoznává. Kód vykonává.**

Model dělá tři věci: rozpozná záměr, vytáhne strukturu, složí text. Všechno ostatní
je deterministický kód. Návrh, ve kterém model něco *vykonává*, je špatný návrh —
a je to první věc, kterou při review hledej.
