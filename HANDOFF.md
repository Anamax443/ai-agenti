# HANDOFF — deník stavu: ai-agenti

Append-only. Nejnovější záznam nahoru. Slouží k pokračování z jiného počítače / po pauze.

## 2026-09-01 (4) — riziko má dvě osy: vratnost akce × dopad systému

- **Proč:** externí oponentura (`A3`) ukázala, že klasifikace podle vratnosti akce sama
  nestačí. Agent, který jen čte životopisy a doporučuje pořadí, nemá jedinou nevratnou
  akci — podle §7 tedy nejnižší režim „běž sám, jen informuj". Přitom rozhoduje, kdo se
  dostane k pohovoru, a pro vyřazeného člověka je ta chyba nevratná. Opačně platí totéž:
  „agent s vysokým dopadem" neřekne, které z jeho čtyřiceti volání potřebuje schválení.
- **Hotové — principy §7 přepsané na dvě osy** (CS i EN):
  - **osa akce** (vratnost) určuje **režim** jednotlivé akce — beze změny, jen pojmenovaná,
  - **osa systému** (dopad) určuje **přísnost**, s jakou se všechno ověřuje. Pět otázek:
    kdo je předmětem rozhodnutí · co ovlivní · s jakými daty · v jakém rozsahu · pozná se
    chyba včas. Z odpovědí plyne stupeň **N / Z / V**.
- **Přísnost něco mění, jinak by to byl další štítek.** Tabulka „co přísnost mění" váže
  stupeň na zjednodušení fází, povinné těžké zápory v evalech, **minimální stupeň
  uzavření nálezu** (N → U1, Z → U2, V → U3), adresáta hlášení, dohled a periodu revize
  scénářů. U stupně **V** navíc: rozhodnutí o člověku má člověka v kruhu **i když je
  vratné** — vrátit se dá zápis, ne to, že se na někoho nedostalo.
- **Tím padá i `N5`.** Tabulka „Co u malého agenta přeskočit" už nestojí na subjektivním
  „jednoduchý agent pro sebe sama". Nově: zjednodušit smíš jen při přísnosti **N** a
  zároveň bez nevratné reputační či fyzické akce; platí-li jen jedno, jde zjednodušit
  všechno kromě F4 a F5; neplatí-li ani jedno, předpis platí celý. Důvod je v textu:
  každý autor svého agenta zná a považuje ho za jednoduchý, protože zná jeho **záměr** —
  vratnost a dopad záměr neznají, jen následek.
- **Brána F0** dostala položku: přísnost je **odvozená z odpovědí** v návrhovém listu,
  ne odhadnutá, a je napsané, co z ní plyne.
- **Návrhový list** má novou sekci *Přísnost — osa systému*: pět otázek s odpověďmi
  a zaškrtávacím sloupcem, výsledný stupeň a řádek „co z toho plyne". Nevyplňuje se stupeň,
  vyplňují se odpovědi.
- **Oprava vlastní nepřesnosti.** Nález `N5` (a `O2` z posudku P2) tvrdil, že štítek
  „Riziková kategorie (AI Act)" nemá **žádný** důsledek. Přesnější je: jeden důsledek měl
  („u toho se předpis nezkracuje"), ale jen jako věta v návrhovém listu — nebyl navázaný
  na brány ani na tabulku zjednodušení. Teď je.
- **Kvalifikováno tvrzení o AI Actu** (nález `B8`): řádek o označování AI nově zní „podle
  role a jurisdikce; naše pravidlo: vždy" místo „povinné (AI Act)". Právní posouzení tím
  není hotové — jen se přestalo vydávat interní pravidlo za obecnou zákonnou povinnost.
- **Ověřeno:** `python kontrola/dvojice.py` — zelené.
- **Poznámka k tagu `audit-2-freeze`:** ten ukazuje na `85a45cd` a je cílem druhého auditu.
  Tahle změna je **až za ním** a do auditu nevstupuje — jinak by to bylo zase zpětné
  doladění (nález `B7`).
- **Zbývá:** `N3` stavový model · `N1` důkazní pětice v předpisu · `N4` kontrakt rolí
  a metriky podle role modelu · `A6` vrstva bezpečnosti nástrojů (allowlist, validace
  argumentů, výstupní kontrola, testy exfiltrace) · `A4` rozdělení eval sad na regresní /
  challenge / skrytou · `A2` zúžení rozsahu „libovolný agent" · `N6` ukončení · `N8`
  strojová kontrola konzistence. A pořád především: **druhý audit**.

## 2026-09-01 (3) — nosná věta opravena: tři stavy místo dvou; oponentura našla, co osm vlastních nálezů nenašlo

- **Proč:** tři externí posudky podkladu. Nejostřejší nález (`A1`) říká, že věta „buď proces
  selže s hlášením, nebo dopadne dobře; **třetí možnost neexistuje**" je u vzdáleného volání
  technicky nepravdivá: odeslání proběhne, odpověď se ztratí, agent neví, jestli opakovat.
  Výsledek není ani známý úspěch, ani známé selhání. Metodika si navíc odporovala — audit
  JobWatche už žádal stavy `failed`/`degraded`/`notification_pending`, tedy víc než dva konce.
- **Hotové — nosná věta přeformulována** (CS i EN, 15 souborů, 18 zásahů): úspěch · selhání ·
  **zaznamenaný neznámý výsledek**; *tichá* větev neexistuje. Původní tvrzení zůstává platné
  v tom, co chtělo říct — žádný konec nesmí být tichý. Změněno v `PRINCIPY` (§1, §11, §15, §16),
  `BUILD-PREDPIS` (F3 + nepřeskočitelné minimum), `README`, `AGENTS`, `STATUS`, `mapa-mysleni`,
  `manazerske-shrnuti`, `vyvojovy-diagram`.
- **Brána F3 dostala dvě položky:** neznámý výsledek má vlastní stav a další krok (dotaz na
  cílový systém / idempotentní opakování / fronta pro člověka — nikdy naslepo a nikdy `ok`),
  a mezi vyvolaná selhání přibyl **timeout po odeslání a před zápisem**.
- **Nový antivzor:** *Neznámý výsledek zapsaný jako úspěch.*
- **Nezměněno záměrně:** citace v `00-zdroje/ZDROJE.md` (záznam toho, co řekl zdroj, ne naše
  tvrzení) a znění brány citované v `02-pripady/AUDIT-job-watch.md` (historický stav auditu).
- **Uzavřeno taky `B1`:** commit `62d4b38` byl pushnutý až po prvním kole oponentury. Podklad
  ho uváděl jako verzi předmětu, přitom na `origin/main` byl `ed0b7bb` — oponent nemohl nic
  reprodukovat. **Poučení: verze citovaná v dokumentu pro třetí stranu musí být venku dřív
  než dokument.**
- **Ověřeno:** `python kontrola/dvojice.py` — zelené.
- **Zbývá:** sjednotit počet podmínek bran (po dnešní změně je jich **42**, z toho 3 s ověřitelným
  artefaktem a **39** prokazovaných tvrzením — podklad uváděl chybně 38/37); vrátit „důkazní čtveřici"
  na **pětici** včetně artefaktu (příkaz sám není důkaz, důkazem je jeho výstup); rozšířit
  model rizika o systémovou osu vedle vratnosti akce; oddělit regresní / challenge / skrytou
  eval sadu; kvalifikovat tvrzení o AI Actu. A pořád: druhý audit na agentovi jiné třídy.

## 2026-09-01 (večer, 2) — oprava se rozvedla do souhrnů; předpis dostal acceptance testy a těžké zápory

- **Proč:** commit `ed0b7bb` opravil tělo auditu, ale zelené tvrzení zůstalo tam, kam se čtenář
  dívá první — v nadpisu dohry, v řádku tabulky nálezů, v pilulce ve `STATUS.html`, u čísla
  „precision 100 %" a v manažerském shrnutí. **Fajfka přežila nález** — tentýž defekt o patro výš,
  než jaký audit popisuje u JobWatche.
- **Hotové — souhrny uvedeny do souladu s opravou** (CS i EN): nadpis dohry v auditu, řádek
  tabulky u nálezu č. 3 (✅ → ⚠️ z poloviny), číslo za F1 doplněno o výhradu (všech 17 záporů
  odmítne prefiltr, takže precision 100 % nevypovídá o rozlišovací schopnosti), řádek Stav
  a řádek Cizí text ve `STATUS.html`, odstavec dohry v `05-html/manazerske-shrnuti.html`.
- **Hotové — tři změny předpisu**, každá s doloženým případem z druhého kola:
  - **F3 a F6 dostaly acceptance testy vyvolaných selhání.** Tvrzení „dva konce" se prokazuje
    vyvoláním, ne unit testem nad čistou funkcí — čtyři vady v orchestraci JobWatche neodhalilo
    159 testů ani 26 evalů. Přibyly položky: všechny zdroje dolů, selhání po zápisu a před
    odesláním, dva souběžné běhy, zastavení uprostřed, a že zastavený běh zůstane zastavený.
  - **F4 rozlišuje backend z CI a backend jen za běhu** (nezapracovaný bod z 1. 9. dopoledne)
    a nově žádá **těžké zápory** v sadě — zápor, který zahodí deterministický filtr, o modelu
    nevypovídá. Doplněno i do `kostra-agenta/evals/README.md` (složení sady, ne jen počet).
    Doplňkově: obal cizího textu se žádá **na každém volání modelu**, nejdřív tam, kde má model
    nástroje — právě to u JobWatche prasklo.
  - **Oprava rozporu:** kritická cesta zněla `F0 → F1 → F3 → F5`, začímž týž dokument označuje
    za nepřeskočitelný vypínač ve **F6**. Opraveno na `F0 → F1 → F3 → F6`.
- **Ověřeno:** `python kontrola/dvojice.py` — zelené.
- **Zbývá:** druhý audit na agentovi jiné třídy (něco zapisuje nebo posílá ven) — zatím je
  důkazní základna N = 1. Beze změny: smazání `03-projekty/prepisovac/kod/`, `AGENTS.md` do
  ostatních repů, UX kapitola z Albady, Vorel a Lanham, slovník, gwalarn.

## 2026-09-01 — dohra auditu JobWatche: všechny nálezy uzavřené, a jeden nález zpátky do předpisu
- **Hotové:** do [`02-pripady/AUDIT-job-watch.md`](02-pripady/AUDIT-job-watch.md) přibyla sekce
  **Dohra**. Za dva dny padly všechny čtyři nálezy, a to v pořadí, které audit sám předepsal
  (hlášení o pádu → vypínač → obal cizího textu → evaly a verze promptu). **F1 dostalo číslo:**
  přesnost skórování změřena na 23 reálných inzerátech uvnitř nasazené verze — precision 100 %,
  recall i efektivní recall 100 %, coverage 100 %.
- **Nález DO PŘEDPISU (nezapracovaný, návrh):** brána F4 žádá „evaly běží v CI". U agenta, jehož
  výchozí backend je **binding dostupný jen za běhu** (Cloudflare Workers AI), je to nesplnitelné
  — v CI by se měřil jiný model než ten, který rozhoduje. Sada v JobWatchi na to dvakrát doplatila:
  poprvé volala placený model napřímo, podruhé nepředávala volbu backendu, takže měřila free příčku
  i při zvoleném placeném modelu. **Návrh:** u F4 rozlišit backend dostupný z CI (dnešní znění)
  a backend existující jen za běhu („na nasazené verzi, ručně, s protokolem, a v běhu je zapsané,
  která příčka odpověděla"). Bez toho brána nutí buď lhát, nebo měřit vedle.
- **Druhý poznatek:** *zelená sada přestává rozlišovat.* Po opravách je JobWatch 23/23, čímž se
  z měřicího přístroje stává ozdoba. F8 („evaly rostou") tedy není administrativa, ale podmínka,
  aby měření dál něco znamenalo.
- **Aktualizováno:** `STATUS.html` + `.en.html` (tři vady → čtyři, všechny opravené, přidané číslo
  za F1), `05-html/manazerske-shrnuti.html` + `.en.html` (odstavec o dohře).
- **Zbývá:** zapracovat návrh úpravy F4 do `sablony/BUILD-PREDPIS.md` — zatím je jen popsaný
  v auditu, samotný předpis se nemění.

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
  STATUS, deník, obě portfolia v `04-firemni/`, všechny tři dokumenty gwalarnu, zadání
  přepisovače a obě zbývající stránky (`postup-stavby`, `navrhovy-list-faktury`).
  **Kontrola dvojic je zelená: 28 dokumentů v obou jazycích, 1 vedená výjimka.**
- **Nová funkce nese vlastní kontrolu:** [`kontrola/dvojice.py`](kontrola/dvojice.py) ověří,
  že ke každému českému dokumentu existuje anglické dvojče a naopak. Výjimky se zapisují
  ručně do `kontrola/bez-prekladu.txt` — chybějící překlad má být vidět, ne tiše zmizet.
  Zapojeno do CI vedle gitleaks a lychee. Skript zároveň hlásí *zbytečnou* výjimku,
  takže se seznam sám uklidí, až soubor zmizí.
- **Rozpracované:** —
- **Zbývá:**
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
