# VYDÁNÍ v0.11 — 2. 9. 2026

> 🇨🇿 Čeština · [🇬🇧 English](VYDANI.en.md)

| | |
|---|---|
| **Verze** | `v0.11` |
| **Datum** | 2. 9. 2026 |
| **Rozsah** | 50 podmínek v devíti branách, F0–F8 |
| **Známá chyba** | **záchytnost 4 z 8** na jediném doloženém případu |
| **Opakovatelnost** | **neměřena** |
| **Předchozí vydání** | `v0.10` (2. 9. 2026) |
| **Cíl druhého auditu** | **`v0.11`** — značka `audit-2-freeze` je překonaná, viz níž |

Tohle není finální dokument a záměrně se tak nejmenuje. Je to **vydání**: pevný bod, proti
kterému se dá měřit, se zapsanou vlastní chybou a s hranicí, za kterou neplatí.

---

## Změny proti v0.10 — vícenájemnost

Cílem farem je **jedna farma, víc zákazníků**. Dosud byl celý předpis psaný pro jednoho
vlastníka, a to se v textu nikde nepřiznávalo.

| Změna | Proč |
|---|---|
| **F3** — mezi vyvolaná selhání přibyl *dotaz bez rozlišení nájemce*, který musí **selhat**, ne vrátit cizí data | nejtypičtější a nejdražší vada vícenájemních systémů |
| **F5** — nová podmínka: rozlišení nájemce je **vynucené v dotazu, ne v promptu**, a žádná sdílená vrstva nepřenese kontext mezi nájemci | tvrdé kritérium patří do kódu; doložený důvod je filtr regionu z JobWatche |
| **Principy §6** — *sdílený model je sdílený kontext* | cache promptů, sdílená paměť případů a žebřík příček můžou přenést kontext mezi zákazníky **bez útočníka** |

Podmínek je nově **50** (F5 ze 6 na 7).

**Co to dělá s rozsahem platnosti.** V měření JobWatche vyšlo pět podmínek jako `nelze` —
schvalovací brána, lhůta bez odpovědi, označení AI u třetí strany, podíl eskalací. U vícenájemní
farmy jsou to **reálné požadavky**, ne nesedící brány. Etalon se tím rozšiřuje tam, kde byl
dosud nejužší.

> **Původ nálezu je nepříjemný:** izolaci mezi nájemci zmínil posudek P2 už 1. 9. u otázky `Q3`
> a **do dokumentace se nepřenesla**. Zapsala se z ní jen poškozená odpověď modelu a částečné
> selhání závislostí. Připomnělo to až zadání směru — ne kontrola. To je vlastní `N8`
> („fajfka přežije nález") v jiné podobě: **nález, který se nikam nezapsal, přestal existovat.**

## Změny ve v0.10 proti v0.9

Vydání `v0.9` vzniklo večer 1. 9. a **druhý den se na něm změřil první agent**. Měření nenašlo
novou vadu v předmětu, zato našlo tři v samotném měřidle:

| Nález | Změna |
|---|---|
| `M1` chyběl výsledek **„neměřeno"** — měřič se tlačil do `ne`, což je jiné tvrzení | čtvrtá hodnota; podíl `neměřeno` je nově **metrika poctivosti měření** |
| `M2` **stupeň se vyplňoval jen u `ano`** — u `ne` nešlo rozlišit „vyvolal jsem to" od „přečetl jsem kód" | stupeň se vyplňuje i u `ne`; stupnice se ptá pořád na jedno: *čím to víš* |
| `M3` **přísnost se určovala až při měření**, ačkoli ji žádá F0.4 | hlavička protokolu má řádek *původ přísnosti*; určí-li ji měřič, je to zároveň `ne` u F0.4 |

Počet podmínek se nezměnil (**49**), znění bran taky ne. Změnil se **měřicí přístroj** — a to
stačí na nové vydání, protože měření se starým a novým formulářem nejsou porovnatelná.

**Značka `audit-2-freeze` je překonaná.** Zmrazila stav před dvouosým rizikem, stavovým modelem,
měřicím protokolem i kontrolními vrstvami. Měřit proti verzi, která už neexistuje, by druhý audit
zahodilo. Cílem je `v0.10`; značka zůstává jako historie.

## Proč ne 1.0

Metodika chce být **etalon** — měřidlo, ne dobrý text. Měřidlo musí splňovat věci, které dobrý
text splňovat nemusí, a dvě z nich splněné nejsou:

- **Opakovatelnost je neznámá.** Etalon, který umí použít jen jeho autor, není etalon. Ověřuje
  se jediným způsobem — dva měřiči, tentýž agent, tentýž formulář, a rozdíl mezi formuláři se
  odečte. Nikdo to zatím neudělal.
- **Důkazní základna je N = 1.** Jeden audit, na agentovi autora metodiky, který nic nezapisuje
  do cizích systémů a nekomunikuje s cizími lidmi.

Číslo 1.0 by tvrdilo víc, než je doložené. Proto 0.11.

## Známá chyba: 4 z 8

Etalon musí znát svou nepřesnost. Tady je jediné číslo, které o sobě má:

Při prvním ostrém použití našel předpis **čtyři z osmi** vad, které se u téhož agenta nakonec
prokázaly. Chytil vypínač, který nezastavil pipeline · tiché selhání běhu · cizí text bez obalu ·
neměřitelný prompt. **Neodhalil ani jednu ze čtyř vad v orchestraci:** zelený běh při selhání
všech zdrojů, ztracenou notifikaci, chybějící zámek běhu a zastavený běh přepsaný na úspěšný.

**Záchytnost 50 % na jednom vzorku.**

> Že by dnešní znění chytilo 8 z 8, **není měření.** Ty položky z těch vad vznikly, takže by šlo
> o zpětné doladění. Proto se měří vždy proti **vydání**, ne proti aktuálnímu `main`.

## Rozsah platnosti

Metodika se dosud popisovala jako použitelná na „libovolného agenta pro libovolnou doménu". To
tvrzení není doložené a tohle vydání ho zužuje.

**Platí pro** agenta, který má:

- uzavřený seznam scénářů,
- dělbu *model rozpoznává / kód vykonává*,
- vyjmenovatelné nevratné akce.

**Neověřeno pro:**

| Třída agenta | Proč to nevíme |
|---|---|
| plánovací, rešeršní a multiagentní systémy | volí si další krok samy — jádro s nimi nepočítá |
| agenti zapisující do cizích systémů (ERP, účetnictví) | F3 nemá transakce ani kompenzace, F5 nemá schvalování pro víc rolí |
| agenti provozovaní někým jiným než autorem | čitelnost metodiky pro cizího člověka není doložená |
| domény s tvrdými pravidly (účetnictví, výroba, zdravotnictví) | hranice model/kód pod regulačním tlakem nebyla zkoušena |

Není to seznam toho, kde metodika nefunguje. Je to seznam toho, kde **nevíme**, jestli funguje.

## Co přineslo vydání v0.9

Všechno vzniklo 1. 9. 2026 z auditu, jeho dohry a tří externích posudků. Ve v0.10 to platí beze změny.

| Změna | Původ |
|---|---|
| **Tři stavy místo dvou** — pozorovatelný konec: úspěch · selhání · zaznamenaný neznámý výsledek | externí nález `A1`/`N9`: „třetí možnost neexistuje" u vzdáleného volání neplatí |
| **Dvě osy rizika** — vratnost akce určuje režim, dopad systému určuje přísnost N/Z/V | externí nález `A3`; vratnost sama misklasifikuje agenta, který jen čte a doporučuje |
| **Stavový model** — nevratná akce leží na přechodu, ne uvnitř stavu | `N3`: tři ze čtyř orchestračních vad byly jeho chybějící verzí |
| **Odchozí identita a vlastník dat** ve F5 | firemní schránka není schránka vlastníka agenta |
| **Měřicí protokol** a inventář bran (`kontrola/brany.py`, `sablony/MERENI.md`) | audit volným textem je neporovnatelný; počet podmínek se třikrát rozešel |
| **Kontrolní vrstvy** — co která strukturálně nevidí | 159 testů nechytilo osm vad; šíře sama nestačí |
| **Acceptance testy vyvolaných selhání** ve F3 a F6 | druhé kolo nálezů |
| **Těžké zápory** a rozlišení CI/runtime backendu ve F4 | eval sada bez těžkých záporů vyrobila precision 100 %, která nic neznamená |

## Co je jen tvrzené

Podle vlastní stupnice: **všechny změny výše jsou na stupni `U1`** — v textu, dají se přečíst,
**nebyly vyvolány**. Žádný projekt podle nich ještě neprošel měřením.

Konkrétně chybí:

- acceptance test „timeout po odeslání a před zápisem" — v žádném projektu neexistuje,
- vyplněný stavový model u agenta s nevratnou akcí,
- doložený úlovek u nových kontrolních vrstev.

**První vyplněný protokol už existuje** — [`MERENI-job-watch.md`](02-pripady/MERENI-job-watch.md),
2. 9. 2026. Nenašel novou vadu v předmětu, zato tři v měřidle; jsou zapracované ve v0.10.

## Co vydání netvrdí

- **Netvrdí, že je metodika hotová.** Sedm nálezů proti ní zůstává otevřených: důkazní pětice
  v předpisu, kontrakt rolí a metriky podle role modelu, vrstva bezpečnosti nástrojů, rozdělení
  eval sad na regresní/challenge/skrytou, ukončení agenta, strojová kontrola konzistence
  a rozsah platnosti.
- **Netvrdí nic o právu.** Tvrzení o AI Actu jsou v tomto vydání kvalifikovaná jako **interní
  pravidlo, ne citace zákona**. Právní posouzení patří někomu, kdo na to je.
- **Netvrdí, že obal cizího textu uzavírá prompt injection.** Je to obrana v hloubce. Chybí
  allowlist nástrojů a domén, validace argumentů proti schématu, výstupní kontrola a testy
  exfiltrace.
- **Netvrdí, že je zdejší hodnocení nezávislé.** Vzniklo z práce autora metodiky nad vlastním
  agentem, s pomocí tří externích posudků, z nichž jeden byl podepsán autorem samotným.

## Jak se proti tomuto vydání měří

```bash
python kontrola/brany.py --protokol v0.11 > 02-pripady/MERENI-<agent>.md
```

Pravidla vyplňování jsou v [`sablony/MERENI.md`](sablony/MERENI.md). Podstatné je:
`nelze` je plnohodnotný výsledek, u `ano` je povinný důkaz, a **příkaz sám důkaz není** —
důkazem je jeho výstup.

Poziční identifikátory (`F3.4`) platí **uvnitř tohoto vydání**. Po vložení podmínky se posunou;
jejich význam pevně určuje verze, stejně jako u `ISO 27001:2013 A.9.2.3`.

## Co udělá z tohoto vydání 1.0

Ne psaní. Tyhle čtyři věci, v tomhle pořadí:

1. **Druhý audit** na agentovi jiné třídy — ideálně takovém, který zapisuje do cizího systému
   nebo komunikuje ven. Proti zmrazené verzi, s predikcemi zapsanými předem.
2. **Test opakovatelnosti** — dva měřiči, tentýž agent, odečíst rozdíl.
3. **Třetí případ vedený cizím člověkem** — jediný test čitelnosti bez autora.
4. **Záchytnost změřená znovu** na případu, ze kterého pravidla nevznikla.

Do té doby je to velmi dobře zdokumentovaná zkušenost z jednoho agenta. To není málo — ale
jmenuje se to tak, jak to je.

## Historie vydání

| Verze | Datum | Poznámka |
|---|---|---|
| `audit-2-freeze` | 1. 9. 2026 | zmrazeno pro druhý audit; **překonáno** — cílem je `v0.11` |
| `v0.9` | 1. 9. 2026 | první číslované vydání: tři stavy, dvě osy rizika, stavový model, měřicí protokol, kontrolní vrstvy |
| `v0.10` | 2. 9. 2026 | protokol po první zkoušce: výsledek `neměřeno`, stupeň i u `ne`, původ přísnosti |
| `v0.11` | 2. 9. 2026 | vícenájemnost: izolace nájemců ve F3 a F5, sdílený model = sdílený kontext |
