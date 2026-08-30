# AGENTI PRO MALOU KANCELÁŘ

Portfolio agentů, sdílená infrastruktura a provozní praxe.
Postaveno na principu „AI rozpoznává, kód vykonává" a na běžných
DevOps zvyklostech přenesených na práci s modely.

Verze 1.0 · srpen 2026

---

## Část A — Které agenty stavět

### Pořadí podle poměru užitku a rizika

| # | Agent | Ušetří | Riziko chyby | Stavba |
|---|---|---|---|---|
| 1 | **Triáž pošty a helpdesku** | 30–60 min denně | nízké, jen třídí | 3 dny |
| 2 | **Doklady a faktury** | 2–4 h měsíčně | střední, peníze | 5 dní |
| 3 | **Hlídač lhůt a smluv** | zabrání pokutám | nízké | 2 dny |
| 4 | **Zápisy ze schůzek** | 1–2 h týdně | nízké | 3 dny |
| 5 | **Triáž provozních hlášení** | šum v mailu | střední, přehlédnutí | 4 dny |
| 6 | **Onboarding a offboarding** | 1–2 h na osobu | vysoké, oprávnění | 8 dní |

Stavěj v tomhle pořadí. První tři nesahají na nic nevratného a postaví
sdílenou infrastrukturu, na které pojede zbytek.

---

### 1 · Triáž pošty a helpdesku

Nejlepší první agent. Nic nemění, jen třídí — a přesto ušetří nejvíc.

**Vstup:** sdílená schránka `podpora@`, `it@`
**Model dělá:** klasifikaci (kategorie, naléhavost, kdo to má řešit) a shrnutí do tří vět
**Kód dělá:** založení tiketu, přiřazení, notifikaci, deduplikaci vláken
**Brány:** žádné — nic nevratného. Chybné zařazení opraví člověk jedním klikem.

```
mail → [model: kategorie + priorita + shrnutí] → kód: tiket, přiřazení, upozornění
                                               → ranní přehled: co přišlo, co čeká
```

Nenech ho odpovídat zákazníkům. Ať navrhne odpověď jako koncept, který
někdo odešle. Odpověď je nevratná, zařazení není.

---

### 2 · Doklady a faktury

Podrobně rozepsáno v samostatném návrhovém listu. Shrnutí:

**Model dělá:** pozná, že jde o doklad, a dvakrát nezávisle přepíše obsah
**Kód dělá:** porovná oba přepisy, spáruje dodavatele podle čísla účtu,
zkontroluje limit, zapíše do účetního systému
**Brány:** neshoda přepisů → dotaz; nový dodavatel nebo částka nad limit → schválení

V malé firmě bych **nešel až k platbě.** Konec procesu je připravený doklad
v účetnictví se schvalovacím krokem, který zůstává lidský. Rozdíl v ušetřeném
čase je malý, rozdíl v riziku velký.

---

### 3 · Hlídač lhůt a smluv

Nejlevnější agent s nejlepším poměrem. Většina práce je jednorázové naplnění dat.

**Model dělá:** ze smlouvy nebo faktury vytáhne datum konce, výpovědní lhůtu, částku
**Kód dělá:** hlídá kalendář, upozorňuje s předstihem podle typu
**Brány:** žádné, jen upozorňuje

Hlídej: licence, podpory, pojistky, nájmy, revize, certifikáty, domény,
platnost tokenů k API. To poslední se vymstí právě u agentů samotných.

---

### 4 · Zápisy ze schůzek

**Vstup:** nahrávka nebo hlasová zpráva
**Kód dělá:** přepis přes whisper — lokálně, nahrávky z jednání nepatří do cizí služby
**Model dělá:** shrnutí, rozhodnutí, úkoly s odpovědnými
**Brány:** zápis jde ke schválení tomu, kdo schůzku vedl, teprve pak se rozešle

Přepisovací modul už máš. Tohle je nadstavba nad ním.

---

### 5 · Triáž provozních hlášení

**Vstup:** hlášení z monitoringu, antiviru, zálohování, síťových prvků
**Model dělá:** shrne, co se stalo, a odhadne závažnost
**Kód dělá:** deduplikace, prahy, eskalace, ticho v noci u nezávažného
**Brány:** nic neopravuje sám

Past: agent, který má „vyřešit" incident. Nemá. Má z padesáti hlášení
udělat tři věty a říct, které jedno stojí za pozornost.

---

### 6 · Onboarding a offboarding

Nejvyšší riziko z celého portfolia, protože se dotýká oprávnění.

**Model dělá:** z požadavku vytáhne jméno, pozici, nástup, útvar
**Kód dělá:** všechno ostatní — účet, skupiny, schránka, licence, sdílené složky
**Brány:** schválení před založením, druhé schválení u oprávnění nad rámec šablony

Odchod zaměstnance drž jako **plně deterministický proces bez modelu.**
Vstupem je jméno a datum, nic víc. Nesprávně odebraná oprávnění bolí,
nesprávně ponechaná bolí víc.

---

## Část B — Co postavit jednou pro všechny

Šest agentů neznamená šest systémů. Sdílí většinu vrstev:

```
┌──────────────────────────────────────────────┐
│  KANÁLY      chat · mail · webhook · cron    │
├──────────────────────────────────────────────┤
│  IDENTITA    whitelist, role, oprávnění      │
├──────────────────────────────────────────────┤
│  BRÁNY       schvalování, limity, lhůty      │
├──────────────────────────────────────────────┤
│  MODELY      volání, retry, křížová kontrola │
├──────────────────────────────────────────────┤
│  EVIDENCE    běhy, rozhodnutí, zásahy        │
├──────────────────────────────────────────────┤
│  HLÁŠENÍ     chyby, přehledy, metriky        │
└──────────────────────────────────────────────┘
        ▲          ▲          ▲
     agent 1    agent 2    agent 3
```

**Schvalovací vrstva je společná.** Jeden formát zprávy, jedna tabulka
čekajících úkolů, jedno místo, kde se schvaluje. Když ji každý agent
řeší po svém, po půl roce nikdo neví, co kde čeká.

**Evidence běhů taky.** Jedna tabulka: kdo, kdy, co spustil, jak to
dopadlo, co člověk opravil. Z ní se dělá všechno ostatní.

---

## Část C — Repozitář a verzování

### Monorepo

```
office-agents/
├─ packages/
│  ├─ core/            kanály, identita, brány, evidence
│  ├─ models/          volání modelů, retry, křížová kontrola
│  └─ types/           sdílené typy — fixují se první
├─ agents/
│  ├─ triage-mail/
│  ├─ invoices/
│  ├─ deadlines/
│  └─ …                každý má vlastní prompts/ a evals/
├─ prompts/
│  ├─ identity/        tón a styl firmy, sdílené
│  └─ …
├─ evals/              regresní sady
├─ infra/              schéma DB, migrace, konfigurace
├─ runbooks/           co dělat, když se něco stane
└─ .github/workflows/  nebo .gitlab-ci.yml
```

Jedno repo. Agenti sdílejí typy a jádro; v oddělených repozitářích
se rozejdou během měsíce.

### Prompt je kód

Tohle je hlavní rozdíl proti běžnému projektu a nejčastější místo,
kde to malé firmy odbydou.

- Prompty, osobnost a definice nástrojů **bydlí v repozitáři**, ne v UI
  nějakého nástroje a ne v databázi, kterou nikdo neverzuje.
- Změna promptu prochází **stejným review jako změna kódu.** Pull request,
  druhý pár očí, popis proč.
- Prompt má **verzi** a každý běh si ji zapíše. Bez toho nedohledáš,
  podle čeho vznikl výstup, který fungoval.
- Model a jeho verze jsou v konfiguraci, ne natvrdo v kódu. Až
  poskytovatel model odstaví, měníš jeden řádek.

### Větve

Malá firma, jeden až dva lidé: krátké větve z `main`, PR, squash merge.
Žádný git-flow — na dvou vývojářích je to režie bez užitku.

Konvence commitů (`feat:`, `fix:`, `prompt:`) se vyplatí kvůli tomu,
že `prompt:` odliší změny, které se nedají otestovat jednotkovým testem.

---

## Část D — CI/CD

```
push do větve
   │
   ├─ lint + typy
   ├─ jednotkové testy         (logika, brány, limity)
   ├─ eval sada                (AI části — viz níže)
   ├─ scan tajemství           (blokující)
   └─ build
   │
merge do main
   │
   ├─ nasazení do stage
   ├─ kouřové testy proti stage
   │
   └─ ruční schválení → produkce
```

**Ruční brána před produkcí drž i v malé firmě.** Nasazení agenta, který
sahá na e-maily a peníze, není totéž co nasazení webu.

**Prostředí musí být oddělená.** Stage má vlastní schránku, vlastní testovací
data a **nesmí umět odeslat nic ven.** Nejdražší chyba při vývoji agenta
je rozeslání testovacích zpráv skutečným lidem — deaktivuj odesílací
kanály na úrovni konfigurace, ne pomocí `if`.

**Tajemství:** GitHub Actions secrets nebo GitLab CI variables, do produkce
přes Workers Secrets. Nikdy v repozitáři. Zapni skenování tajemství
a přidej `pre-commit` hook — commitnuté přihlašovací údaje se totiž
z historie odstraňují mizerně.

**Závislosti:** Dependabot nebo Renovate, automatické PR, sloučení
po zeleném CI.

---

## Část E — Evaluace

Bez ní nepoznáš, že úprava promptu rozbila něco jiného. Je to obdoba
regresních testů a v projektu s modely je ještě potřebnější, protože
změna je netransparentní.

**Jak na to prakticky:**

1. Sesbírej 20–40 reálných vstupů na agenta — skutečné e-maily, doklady, věty
2. Ke každému zapiš očekávaný výstup: kategorii, vytažená pole, rozhodnutí
3. Napiš skript, který je pustí a spočítá shodu
4. Pusť ho v CI při každé změně promptu

Prahy: u klasifikace míří na 90 % a více; u extrakce polí hodnoť
**pole po poli**, ne celý výstup jako jeden test — jinak se ztratí informace,
kde přesně to selhává.

Sada roste ze selhání. Kdykoli agent v provozu udělá chybu, přidej ten
vstup do sady. Po roce máš materiál, který se nedá koupit.

---

## Část F — Provoz

| Oblast | Minimum pro malou firmu |
|---|---|
| **Účty** | vlastní servisní účet pro agenta, ne osobní účet správce |
| **Oprávnění** | jen na to, co dělá; čtení místo zápisu, kde to stačí |
| **Tokeny** | evidované, s datem expirace, obnova hlídaná agentem č. 3 |
| **Zálohy** | denní export databáze, měsíčně vyzkoušet obnovu |
| **Logy** | běhy 90 dní, rozhodnutí navždy, obsah zpráv co nejkratší dobu |
| **Vypínač** | jedna zpráva zastaví frontu; runbook říká kdo a jak |
| **Náklady** | týdenní hlídání útraty za API, upozornění při překročení |
| **Runbooky** | co dělat, když spadne kanál, vyprší token, změní se API |

**Osobní údaje:** e-maily a doklady je obsahují. Zapiš, co se posílá do
modelu, jak dlouho se to drží a kdo k tomu má přístup. V malé firmě to
je stránka textu, ale musí existovat dřív, než se agent zapne.

**Zastupitelnost.** Když agenta postavíš sám a nikdo jiný neví, jak funguje,
je to riziko srovnatelné s tím, které měl nahradit. Runbooky a diagram
toku jsou minimum.

---

## Část G — Zavádění

| Fáze | Obsah | Doba |
|---|---|---|
| 0 | Repozitář, CI, prostředí, evidence běhů, schvalovací vrstva | 1 týden |
| 1 | Agent 1 v režimu „jen navrhuje" — nic nemění, jen třídí do konceptu | 3 dny |
| 2 | Agent 1 ostře, měsíc sledování, sběr chyb do eval sady | 1 měsíc |
| 3 | Agenti 2 a 3 na hotové infrastruktuře | 1 týden |
| 4 | Zbytek podle potřeby | — |

**Fáze 1 je klíčová a přeskakuje se nejčastěji.** Nech agenta měsíc běžet
naprázdno vedle stávajícího postupu a porovnávej, co by udělal, s tím,
co udělal člověk. Vyjde z toho eval sada i důvěra.

---

## Část H — Co nedělat

- **Neřešit vše jedním agentem.** Šest úzkých je levnějších a spolehlivějších
  než jeden široký.
- **Nedávat agentovi zápis do produkčních systémů dřív než po měsíci čtení.**
- **Neschovávat prompty do databáze bez verzování.** Přestane jít dohledat,
  proč se něco stalo.
- **Nenechat agenta odpovídat cizím lidem bez schválení.** Ani „jen potvrzení".
- **Nespouštět bez vypínače.** Musí existovat jeden příkaz, který to zastaví.
- **Nestavět offboarding jako první.** Vypadá to jako jednoduchá automatizace
  a je to nejrizikovější věc v seznamu.
