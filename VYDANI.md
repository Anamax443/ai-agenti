# VYDÁNÍ v0.9 — 1. 9. 2026

> 🇨🇿 Čeština · [🇬🇧 English](VYDANI.en.md)

| | |
|---|---|
| **Verze** | `v0.9` |
| **Datum** | 1. 9. 2026 |
| **Rozsah** | 49 podmínek v devíti branách, F0–F8 |
| **Známá chyba** | **záchytnost 4 z 8** na jediném doloženém případu |
| **Opakovatelnost** | **neměřena** |
| **Předchozí značka** | `audit-2-freeze` — verze zmrazená pro druhý audit |

Tohle není finální dokument a záměrně se tak nejmenuje. Je to **vydání**: pevný bod, proti
kterému se dá měřit, se zapsanou vlastní chybou a s hranicí, za kterou neplatí.

---

## Proč ne 1.0

Metodika chce být **etalon** — měřidlo, ne dobrý text. Měřidlo musí splňovat věci, které dobrý
text splňovat nemusí, a dvě z nich splněné nejsou:

- **Opakovatelnost je neznámá.** Etalon, který umí použít jen jeho autor, není etalon. Ověřuje
  se jediným způsobem — dva měřiči, tentýž agent, tentýž formulář, a rozdíl mezi formuláři se
  odečte. Nikdo to zatím neudělal.
- **Důkazní základna je N = 1.** Jeden audit, na agentovi autora metodiky, který nic nezapisuje
  do cizích systémů a nekomunikuje s cizími lidmi.

Číslo 1.0 by tvrdilo víc, než je doložené. Proto 0.9.

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

## Co je v tomto vydání nové

Všechno vzniklo 1. 9. 2026 z auditu, jeho dohry a tří externích posudků.

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
- první vyplněný měřicí protokol,
- doložený úlovek u nových kontrolních vrstev.

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
python kontrola/brany.py --protokol v0.9 > 02-pripady/MERENI-<agent>.md
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
| `audit-2-freeze` | 1. 9. 2026 | verze zmrazená pro druhý audit; záchytnost 4/8 |
| `v0.9` | 1. 9. 2026 | první číslované vydání: tři stavy, dvě osy rizika, stavový model, měřicí protokol, kontrolní vrstvy |
