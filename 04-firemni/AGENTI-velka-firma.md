# AGENTI VE VELKÉ FIRMĚ

Platforma, správa a portfolio. Navazuje na dokument pro malou kancelář,
ale řeší jiný problém.

Verze 1.0 · srpen 2026

---

## Část A — Co se mění

V malé firmě je otázka „kterého agenta postavit". Ve velké firmě je
otázka **„jak umožnit, aby si agenty stavěly týmy samy, a přitom
nevznikl nespravovatelný zvěřinec".**

| | Malá firma | Velká firma |
|---|---|---|
| Kdo staví | jeden člověk | desítky lidí v různých útvarech |
| Hlavní riziko | agent udělá chybu | nikdo neví, kolik agentů běží a k čemu mají přístup |
| Těžiště práce | agenti | platforma a pravidla |
| Schvalování | jeden člověk v chatu | role, zastupitelnost, oddělení pravomocí |
| Náklady | pod hranicí zájmu | rozúčtování na střediska |
| Regulace | okrajově | AI Act, GDPR, interní audit |

Když se to postaví jako řada samostatných projektů, po roce běží čtyřicet
agentů, každý s vlastním způsobem volání modelů, vlastními přístupovými
údaji a bez evidence. Rozplést to je pak dražší než postavit to znovu.

**Stavěj tedy nejdřív platformu, pak agenty.**

---

## Část B — Platforma

### Brána k modelům

Jediné místo, kudy prochází každé volání modelu v celé firmě.

```
agenti a aplikace
        │
        ▼
┌───────────────────────────────────────────┐
│  BRÁNA K MODELŮM                          │
│  ověření volajícího · limity · rozúčtování│
│  redakce osobních údajů · záznam volání   │
│  směrování na model · záložní model       │
└───────────────────────────────────────────┘
        │
   poskytovatelé
```

Co tím získáš:

- **Rozúčtování.** Každé volání nese středisko a agenta. Bez toho nikdo
  neví, kdo utrácí.
- **Verze modelu na jednom místě.** Poskytovatel model odstaví — měníš
  konfiguraci, ne třicet aplikací.
- **Záznam.** Auditní stopa všech volání, oddělená od aplikačních logů.
- **Ochrana údajů.** Redakce rodných čísel, čísel účtů a podobných polí
  na jednom místě, ne v každém agentovi zvlášť.
- **Limity.** Strop na agenta i na středisko, aby chyba v cyklu nevyžrala
  měsíční rozpočet za noc.

Nemusí to být složité — reverzní proxy s autentizací, logem a limity.
Ale musí to být povinná cesta. Přímá volání poskytovatelů blokuj na firewallu.

### Sdílené služby

Postav jednou, používají všichni:

| Služba | Co dělá |
|---|---|
| **Schvalovací fronta** | jedno místo, kde lidé schvalují cokoli od kteréhokoli agenta |
| **Evidence běhů** | kdo, kdy, co spustil, jak dopadlo, co člověk opravil |
| **Katalog nástrojů** | schválené konektory do systémů, s definovanými oprávněními |
| **Knihovna promptů** | firemní tón, sdílené instrukce, verzované |
| **Evaluační běžec** | pouští regresní sady v CI |
| **Šablona agenta** | kostra repozitáře, ze které se startuje |

Šablona je důležitější, než vypadá. Když nová věc vznikne za dvě hodiny
z připravené kostry, nikdo si nebude stavět vlastní.

---

## Část C — Správa a evidence

### Registr agentů

Povinný záznam pro každého agenta v provozu. Bez záznamu nedostane
přístup přes bránu — to je jediný způsob, jak registr udržet živý.

```
NÁZEV
VLASTNÍK              konkrétní člověk, ne útvar
ZÁSTUPCE              kdo to řeší, když vlastník není
ÚČEL                  jednou větou
STŘEDISKO             kdo platí
KATEGORIE RIZIKA      1-4, viz níže
DATA                  jaké kategorie údajů zpracovává
SYSTÉMY               kam sahá, s jakými oprávněními
LIDSKÝ DOHLED         kdo schvaluje, co
STAV                  návrh | pilot | provoz | vyřazen
REVIZE                datum poslední a příští
```

### Kategorie rizika

| | Popis | Co se vyžaduje |
|---|---|---|
| **1** | jen čte a shrnuje, nic nemění | ohlášení, evidence běhů |
| **2** | mění interní data, vratné | schválení vlastníka systému, eval sada |
| **3** | komunikuje ven, sahá na peníze nebo oprávnění | schválení bezpečnosti, lidská brána u každé akce |
| **4** | dopad na osoby — nábor, hodnocení, přístupy | právní posouzení, doložená dokumentace, dohled |

Kategorii určuje **dopad, ne technologie.** Jednoduchý skript, který
odebírá přístupy, je kategorie 3.

### Oddělení pravomocí

Kdo agenta staví, nesmí schvalovat jeho nasazení do provozu ani
jeho vlastní akce. V malé firmě je to nepraktické, ve velké je to
minimum, které bude auditor chtít vidět.

---

## Část D — Regulace

### AI Act, stav k srpnu 2026

Načasování se loni změnilo a hodně interních materiálů je proto neaktuálních.

Nařízení (EU) 2026/1744, tzv. Digital Omnibus, vstoupilo v platnost 27. července 2026, tedy šest dní před původním termínem. Povinnosti pro samostatné vysoce rizikové systémy z přílohy III se posunuly z 2. srpna 2026 na 2. prosince 2027, u AI vestavěné do výrobků podle přílohy I na 2. srpna 2028.

Co se ale **neposunulo:** povinnosti průhlednosti podle článku 50 platí od 2. srpna 2026, tedy už teď. U systémů uvedených na trh před tímto datem platí čl. 50(2) až od 2. prosince 2026, kdy zároveň začínají platit nové zákazy.

Prakticky to znamená:

- **Agent musí přiznat, že je AI**, kdykoli komunikuje s člověkem zvenčí.
  To platí dnes, ne za rok.
- **Odklad neznamená pauzu.** Inventarizace a klasifikace systémů se dělá
  teď; posun je na doložení shody, ne na její přípravu.
- Odklad je vázaný na registrační mechanismus a systémy uvedené do provozu
  před termínem mají výjimku — která ale padá, jakmile systém podstatně změníš.

Sankce jsou vysoké: zakázané praktiky až 35 milionů eur nebo 7 % obratu,
porušení průhlednosti a pravidel pro vysoce rizikové systémy do 15 milionů
nebo 3 %.

**Co bývá kategorie 4:** nábor a výběr uchazečů, hodnocení zaměstnanců,
rozhodování o přístupech a povyšování. Tedy přesně ty úlohy, které HR
chce automatizovat jako první.

### Ochrana osobních údajů

- Posouzení vlivu (DPIA) u všeho, co zpracovává osobní údaje ve větším rozsahu
- Smlouva o zpracování s poskytovatelem modelu, ověřená doba uchování
  a to, zda se data používají k trénování
- Záznam o činnostech zpracování doplnit o agenty — na to se zapomíná
- Umístění dat a přeshraniční přenosy

Právní posouzení dělej **před pilotem, ne po něm.** Zastavený pilot,
do kterého se investovalo čtvrt roku, je horší než odložený start.

---

## Část E — Identita a oprávnění

- **Vlastní servisní identita pro každého agenta.** Ne sdílený účet,
  ne osobní účet správce. V prostředí Entra ID spravovaná identita
  nebo aplikační registrace s certifikátem, ne heslo.
- **Nejmenší možná oprávnění.** Čtení místo zápisu, jedna schránka místo
  celého tenantu, jedna databáze místo serveru.
- **Časově omezená vyšší oprávnění.** Když agent potřebuje víc, ať je
  dostane na dobu úkolu a se záznamem.
- **Agent nesmí dědit práva uživatele**, který ho spustil. Jinak se
  oprávnění tiše rozlézají.
- **Střídání přihlašovacích údajů** automaticky, s hlídáním expirace.
- **Odchod zaměstnance** musí odebrat i jeho agenty. Osiřelý agent
  s platnými oprávněními je klasická díra.

---

## Část F — Portfolio podle útvarů

| Útvar | Agent | Riziko | Poznámka |
|---|---|---|---|
| IT | triáž tiketů, návrh odpovědi | 1–2 | dobrý první |
| IT | shrnutí provozních hlášení | 2 | netřídí sám incidenty |
| IT | příprava účtů podle šablony | 3 | zápis až po pilotu |
| Finance | přepis a párování dokladů | 2–3 | konec u schválení, ne u platby |
| Finance | hlídání lhůt a smluv | 1 | nejlepší poměr |
| Nákup | porovnání nabídek | 2 | rozhoduje člověk |
| Obchod | příprava podkladů před schůzkou | 1 | čte CRM, nic nemění |
| Obchod | návrh odpovědi na poptávku | 2 | odesílá člověk |
| Právní | vytažení termínů ze smluv | 2 | nenahrazuje posouzení |
| HR | třídění životopisů | **4** | příloha III, doložený dohled |
| HR | odpovědi na dotazy k benefitům | 1 | ze schválené znalostní báze |
| Provoz | zápisy z jednání | 1 | přepis lokálně |

Nasazuj po řádcích s rizikem 1 a 2. HR nechej naposledy, ne proto,
že je technicky těžké, ale proto, že je regulačně nejdražší.

---

## Část G — Vývoj a nasazení

### Repozitáře

Platforma v jednom repozitáři, agenti ve svých. Opak než u malé firmy —
při desítkách týmů monorepo znamená, že každá změna čeká na cizí CI.

```
platform/            brána, sdílené služby, knihovny, šablona
agent-<nazev>/       jeden repozitář na agenta, ze šablony
```

Platforma vydává verzované knihovny. Agenti je konzumují jako závislost
a aktualizují si je sami, s tím, že staré verze mají oznámenou dobu podpory.

### Zlatá cesta

Připravená trasa, po které se jde nejrychleji: šablona repozitáře,
předpřipravené CI, brána k modelům, katalog nástrojů, registr.
Kdo jde po ní, má nasazeno za den. Kdo z ní chce sejít, potřebuje
schválení a musí zdůvodnit proč.

Zakazovat odchylky nefunguje. Udělat zlatou cestu tak pohodlnou,
že se nikomu nechce odbočovat, ano.

### CI/CD

```
push       → lint · typy · testy · eval sada · scan tajemství · SBOM
merge      → nasazení do vývojového prostředí
             kouřové testy
             ↓
             stage: kompletní data, odesílací kanály vypnuté konfigurací
             ↓
schválení  → produkce (jiná osoba než autor)
```

Povinné brány v CI, které se ve velké firmě vyplatí:

- **Eval sada** s prahem. Pokles pod hranici zastaví nasazení stejně
  jako spadlý test.
- **Změna promptu je změna kódu.** Prochází review, nese verzi,
  zapisuje se do každého běhu.
- **Kontrola oprávnění.** Když se v konfiguraci objeví nový přístup
  do systému, CI to označí a vyžádá schválení bezpečnosti.
- **Skenování tajemství**, blokující, na úrovni organizace.

---

## Část H — Provoz

| Oblast | Co zavést |
|---|---|
| **Sledování** | dashboard na agenta: běhy, chybovost, latence, náklad, podíl lidských zásahů |
| **Trasování** | každý běh dohledatelný krok po kroku i za měsíc |
| **Hlášení incidentů** | agent je systém jako každý jiný, patří do stejného procesu |
| **Vypínač** | centrální, na úrovni brány. Jedním úkonem lze zastavit jednoho agenta i všechny. |
| **Rozúčtování** | měsíčně na střediska, jinak se náklady stanou neviditelnými |
| **Revize** | každý agent jednou za rok: běží ještě? má ještě smysl? nemá zbytečná práva? |
| **Vyřazení** | proces na ukončení: odebrat identitu, uzavřít data, zapsat do registru |

Ukazatel, který se vyplatí sledovat nejvíc: **podíl výstupů, které člověk
před schválením upravil.** Když roste, něco se rozjelo — obvykle změna
na vstupu, ne model.

---

## Část I — Stínové nasazování

Největší reálný problém velkých firem není špatně postavený agent,
ale agenti, o kterých centrálně nikdo neví. Vznikají v odděleních,
běží na osobních účtech a přístupech, nikdo je nereviduje.

Co s tím funguje:

1. **Amnestie.** Vyhlaš období, kdy lze cokoli existujícího nahlásit
   bez postihu, s nabídkou pomoci to převést na platformu.
2. **Zlatá cesta rychlejší než improvizace.** Dokud je oficiální cesta
   pomalejší, budou lidé chodit mimo ni.
3. **Technická hranice.** Blokuj přímý přístup k poskytovatelům modelů
   mimo bránu. Ne jako trest, ale aby stínová cesta prostě nešla.
4. **Nepotrestat prvního, kdo se přizná.** Jinak je to poslední.

---

## Část J — Zavádění

| Měsíce | Obsah |
|---|---|
| 1–2 | Brána k modelům, registr, pravidla, kategorie rizika |
| 2–3 | Šablona agenta, CI, evaluační běžec, schvalovací fronta |
| 3–5 | Dva piloty z kategorie 1, jiné útvary, měsíc naprázdno |
| 5–6 | Vyhodnocení, úprava zlaté cesty podle toho, co pilotům chybělo |
| 6–9 | Otevření platformy dalším útvarům, školení, amnestie |
| 9–12 | Kategorie 3 s doloženým dohledem, příprava na kategorii 4 |

Piloty veď **ve dvou různých útvarech.** Jeden pilot v IT ukáže, že to
funguje pro lidi, kteří to postavili. Druhý ukáže, co chybí v dokumentaci.

---

## Část K — Co nedělat

- **Nezačínat portfoliem agentů.** Bez brány a registru vznikne
  za rok neuklizitelný nepořádek.
- **Nedělat centrální tým, který staví všechno.** Stane se úzkým hrdlem
  a útvary ho obejdou. Má stavět platformu, ne agenty.
- **Nespouštět HR úlohy jako první.** Regulačně nejdražší část portfolia.
- **Nespoléhat na loňské materiály k AI Actu.** Termíny se v červenci
  změnily a část povinností se přitom neposunula.
- **Nedávat agentovi práva uživatele.** Vlastní identita, vlastní rozsah.
- **Nepodcenit vyřazování.** Firma po dvou letech obvykle neví,
  co všechno jí ještě běží.
