# PRINCIPY STAVBY AI AGENTŮ

Obecná metodika, použitelná na libovolného agenta pro libovolnou doménu.
Vznikla z rozboru Skippyho (Marek Bartoš, podcast Keci a politika)
a z praxe návrhu agenta pro kapelu Gwalarn.

Verze 1.0 · srpen 2026

---

## 1. Základní princip

> **AI rozpoznává. Kód vykonává.**

Tohle je jediná věta, ze které plyne skoro všechno ostatní. Model je dobrý
v tom, že z neuspořádaného vstupu pozná, o co jde. Je špatný jako vykonavatel,
protože jeho výstup není zaručený a nejde ho odladit.

Když agent dostane e-mail s fakturou, model má jediný úkol: poznat, že jde
o fakturu. Tím jeho role končí. Přepis, kontrola, párování s dodavatelem
a odeslání platby jsou pevný proces, nad kterým už žádný model nepřemýšlí.

Ze stejné myšlenky plyne bezpečnostní vlastnost, kvůli které to celé stojí za to:

> Každý pokus skončí **pozorovatelným** stavem: známý úspěch, známé selhání,
> nebo zaznamenaný neznámý výsledek.
> **Tichá větev neexistuje.**

Agent, který si sám rozhoduje, jak úkol splní, tuhle vlastnost nemá. Může
uspět, selhat, nebo udělat něco, co nikdo nechtěl — a nikdo se to nedozví.
Ta tichá větev je zdrojem většiny příběhů typu „asistent rozeslal e-mail
padesáti lidem".

**Proč tři stavy, a ne dva.** Do 1. 9. 2026 tu stálo „buď selže s hlášením, nebo
dopadne dobře; třetí možnost neexistuje". U vzdáleného volání to neplatí: odeslání
proběhne, odpověď se ztratí, agent neví, jestli má opakovat. Výsledek není ani známý
úspěch, ani známé selhání — je **neznámý**, a je to řádný stav, ne vada. Vada je,
když se neznámý výsledek zamlčí nebo se naslepo zopakuje: první ztratí účinek, druhé
ho udělá dvakrát. Neznámý výsledek proto má vlastní další krok — dotaz na stav cílového
systému, idempotentní opakování, nebo fronta pro člověka. Původní věta zůstává platná
v tom, co chtěla říct: **žádný konec nesmí být tichý.**

---

## 2. Test: patří to modelu, nebo kódu?

U každé činnosti v systému polož čtyři otázky:

| Otázka | Odpověď „ano" znamená |
|---|---|
| Dá se to popsat jako `if`–`then`? | kód |
| Je vstup strukturovaný (JSON, formulář, DB)? | kód |
| Musí být výsledek pokaždé stejný? | kód |
| Je vstup volný text, řeč, obraz nebo záměr člověka? | model |

Tři nejčastější úlohy pro model:

1. **Rozpoznání záměru** — „co po mně ten člověk chce"
2. **Extrakce struktury** — z věty nebo dokumentu udělat JSON
3. **Syntéza textu** — napsat něco, co má znít jako člověk

Všechno ostatní je obvykle kód. Když si nejsi jistý, zkus úlohu popsat
kolegovi jako postup. Když to jde bez „a pak to nějak posoudí", je to kód.

### Proč na tom záleží ekonomicky

Deterministický proces stojí zlomek toho, co model. Bartoš uvádí, že jeho
agent stojí kolem pěti tisíc měsíčně; kdyby stejnou práci hrnul přes AI,
byly by to desítky tisíc. Rozdíl není v modelu, ale v tom, kolik práce
mu vůbec dá.

---

## 3. Anatomie agenta

```
┌─ VSTUPNÍ KANÁLY ────────────────────────────────────┐
│  chat · hlas · e-mail · webhook · senzor · cron     │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─ ROZPOZNÁNÍ ZÁMĚRU ─────────────────────────────────┐
│  model: o co jde? → jeden ze známých scénářů        │
│  neznámý záměr → dotaz na člověka, nikdy improvizace│
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─ HLAVNÍ MYSL ───────────────────────────────────────┐
│  paměť · kontext · osobnost · oprávnění             │
│  rozhoduje CO se spustí, ne JAK to proběhne         │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─ PEVNÉ PROCESY ─────────────────────────────────────┐
│  deterministický kód · validace · idempotence       │
│  volitelně malý subagent na dílčí úkol              │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─ BRÁNY ─────────────────────────────────────────────┐
│  limity · schválení člověkem · křížová kontrola     │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─ VÝSTUPNÍ KANÁLY ───────────────────────────────────┐
│  zpráva · publikace · zápis do systému · platba     │
└─────────────────────────────────────────────────────┘
```

### Hlavní mysl a subagenti

Jedna hlavní instance drží paměť a kontext. Dílčí práci dělají malé,
levné modely s úzkým zadáním — Skippy má zvlášť „část mozku" na faktury.
Subagent nemá přístup k celé paměti ani k plným oprávněním. Dostane
jen to, co potřebuje na svůj úkol.

Tohle není jen úspora. Subagent s omezeným kontextem se nemá jak splést
způsobem, o kterém neví ani ty.

---

## 4. Osobnost jako artefakt

Osobnost není přepych, je to úspora kontextu. Místo dvaceti pokynů
o tónu stačí jeden odkaz na popis charakteru.

**Jak ji vyrobit:** nesestavuj ji ručně. Seber zdrojový materiál —
u Skippyho to byly e-booky s literární postavou, u kapely to jsou texty
písní, dosavadní příspěvky a bio, u firemního agenta interní komunikace
a manuály. Nechej model napsat analytický popis a ten pak ručně oprav.

Do popisu patří i **negativní vymezení** — čemu se vyhýbat, jaká klišé
nepoužívat. Ta část bývá účinnější než výčet žádoucích vlastností.

Osobnost se propisuje i do subagentů, jinak systém mluví dvěma hlasy.

---

## 5. Vstupy a periferie

Agent je tak použitelný, jak snadno se s ním komunikuje. Rozhraní,
které vyžaduje otevřít notebook, se nepoužije.

| Kanál | K čemu se hodí | Na co pozor |
|---|---|---|
| **Chat (Telegram, WhatsApp)** | hlavní obousměrný kanál | identita podle ID, ne podle jména |
| **Hlasová zpráva** | vstup za chůze, v autě | přepis přes whisper, pak jako text |
| **E-mail** | příchozí úkoly od cizích lidí | vždy přes rozpoznání záměru, nikdy přímo do procesu |
| **Webhook** | události z jiných systémů | ověření podpisu, idempotence |
| **Cron** | plánované a opakované | musí snést dvojí spuštění |
| **Senzor / poloha** | kontext bez ptaní | z polohy a času lze odvodit situaci |
| **Brýle, hodinky** | výstup bez vytažení telefonu | jen krátké zprávy |

**Volba kanálu podle situace.** Skippy pozná z polohy a rychlosti, že
uživatel řídí, a místo textu pošle hlasovku. Tohle je levné na
implementaci a nepřiměřeně to zvyšuje použitelnost.

**Chat vyhrává nad formulářem.** Na mobilu je nadiktovat větu rychlejší
než vyplnit šest polí. Model z věty udělá strukturu, agent ji ukáže
ke schválení. Formulář stavěj až tehdy, když s agentem musí pracovat
někdo, kdo v chatu není.

---

## 6. Oprávnění a identita

**Identita se váže na kanál, ne na jméno.** Telefonní číslo, Telegram ID,
podepsaný webhook. Kdokoli může napsat „tady Nikola" — ale ne z jejího čísla.

Model oprávnění:

```
kdo (identita)  ×  co (akce)  ×  kolik (limit)  =  povoleno / eskalace
```

Praktická pravidla:

- **Whitelist, ne blacklist.** Kdo není uvedený, nemá přístup.
- **Různí lidé různá práva.** U Skippyho má manželka větší oprávnění
  přeskládat kalendář než on sám.
- **Cizí vstup nikdy nespouští akci přímo.** E-mail od neznámého projde
  rozpoznáním záměru a skončí v denním přehledu, ne v procesu.
- **Agent přiznává, že je AI.** Vyžaduje to AI Act, a v praxi to funguje
  líp než opak.

---

## 7. Brány: kdy se ptát člověka

Rozhodující není, jak moc modelu věříš, ale **jak drahá je chyba.**
Bartoš nechává platit faktury bez schválení proto, že peníze od známého
dodavatele se dají vrátit. Ne proto, že by AI věřil.

| Vratnost chyby | Režim | Příklad |
|---|---|---|
| Plná, do minut | běž sám, jen informuj | zápis do kalendáře, štítek v e-mailu |
| Finanční, vymahatelná | pevný proces + limit | platba schválenému dodavateli |
| Nevratná reputačně | **schválení vždy** | veřejný příspěvek, e-mail cizí straně |
| Nevratná fyzicky | schválení + druhý kanál | ovládání zařízení, mazání dat |

Test pro každou akci: *co se stane, když to udělá špatně, a jak dlouho
trvá to vrátit.* Odpověď určí režim.

**Dvě brány místo jedné.** U opakovaných úloh schvaluj plán jednou pro
celou sérii a pak už jen jednotlivé nevratné kroky. Šetří to klikání
bez ztráty kontroly.

---

## 8. Křížová kontrola

Kde na přesnosti opravdu záleží, nech úlohu udělat **dvakrát nezávisle
a porovnej.**

U Skippyho fakturu přepíše Mistral OCR a nezávisle Gemini. Oba modely
pak mají jediný úkol — najít mezi svými výstupy rozdíly. Když se shodnou,
je to skoro jistě správně. Když ne, jde dotaz na člověka.

Kde se to vyplatí: čísla, datumy, částky, jména, identifikátory. Tedy
všude, kde se chyba nepozná pohledem a projeví se až později.

Kde ne: syntéza textu. Dvě různé formulace nejsou spor.

---

## 9. Paměť

Rozliš tři vrstvy — pletou se a každá se chová jinak:

| Vrstva | Obsah | Kde bydlí |
|---|---|---|
| **Trvalá** | osobnost, pravidla, oprávnění | soubor v repozitáři |
| **Faktická** | události, kontakty, historie | databáze |
| **Pracovní** | probíhající konverzace | kontext modelu |

Faktická paměť **nepatří do promptu celá.** Agent si vyžádá jen to,
co k úkolu potřebuje. Jinak náklady i chybovost rostou s časem.

Co si agent ukládá sám, ať ukládá strukturovaně. Volné poznámky
v přirozeném jazyce se po půl roce nedají použít.

---

## 10. Proaktivita

Agent, který jen odpovídá, je nástroj. Agent, který se ozve sám, je asistent.
Rozdíl je většinou pár řádků.

Zdroje proaktivity:

- **Časové** — ráno přehled, před schůzkou připomínka
- **Z mezery** — „byl jsi v té firmě a nic jsi neřekl, mám to ignorovat?"
- **Z prahu** — něco překročilo mez, stojí to za zprávu
- **Z okolí** — nový článek, změna, událost v hlídaném zdroji

Míra je klíčová. Agent, který otravuje, se vypne. Dobré pravidlo:
ozvi se, když **z toho plyne otázka nebo úkol** — ne když se jen
něco stalo.

---

## 11. Selhání a pozorovatelnost

- **Tiché selhání je nejhorší varianta.** Když proces spadne, musí přijít
  zpráva. Agent, který mlčí, vypadá stejně jako agent, který pracuje.
- **Idempotence.** Každý kanál doručuje opakovaně. Klíč z ID zprávy,
  ne z obsahu.
- **Neznámý výsledek je stav, ne chyba.** Vzdálené volání proběhne, odpověď se
  ztratí — agent neví, co se stalo. Ten stav se **zapisuje** (`neznamy`,
  `ceka_na_smireni`) a řeší se dotazem na cílový systém, idempotentním opakováním,
  nebo frontou pro člověka. Nikdy opakováním naslepo a nikdy zápisem `ok`.
- **Vypršení.** Čekání na schválení má lhůtu, po ní se úkol zahodí
  a oznámí.
- **Log obsahuje rozhodnutí, ne jen výsledky.** Proč agent spustil
  zrovna tenhle proces, se za měsíc jinak nedohledá.
- **Vypínač.** Musí existovat způsob, jak agenta zastavit jednou zprávou.

---

## 12. Zlepšování

Nejcennější zpětná vazba nejsou metriky, ale **tvoje zásahy.** Kdykoli
agent něco navrhne a ty to před schválením upravíš, ten rozdíl je přesná
informace „takhle ne, takhle ano". Ukládej obě verze.

Míra zásahu v čase je zároveň diagnostika: když roste, něco se rozjelo —
obvykle osobnost nebo zadání, ne model.

**Změny promptů nikdy neaplikuj automaticky.** Nech si navrhnout novou
verzi s odůvodněním, přečti ji a schval. Automatická smyčka se při malém
vzorku rozjede špatným směrem a poznáš to pozdě.

Verzuj zadání a osobnost, nepřepisuj. Jinak nedohledáš, podle čeho vznikl
výstup, který fungoval.

---

## 13. Modulární rozpad

Agent se nestaví jako celek. Staví se jako sada modulů, které jdou
otestovat samostatně, a teprve pak se propojí.

Každý modul má:

1. **Kontrakt** — vstup a výstup, písemně, předem
2. **Vlastní CLI** — spustitelný bez zbytku systému
3. **Testy** — jednotkové na logiku, integrační na výstup
4. **Bránu** — podmínky, které musí platit, než se prohlásí za hotový

Kontrakty se fixují **dřív než první řádek kódu.** Když M1 vrací string
a M2 čeká objekt, přepisují se oba.

Modul nesahá do cizí databáze. Data dostane jako parametr. Jinak nejde
testovat s podvrženými vstupy a integrace se změní v ladění všeho naráz.

**Pořadí:** nejdřív moduly, které nepotřebují cizí přístupy a jejichž
výstup jde ověřit okem. Ty dávají nejrychleji jistotu, že to půjde.

Po propojení nezkoušej všechno naráz. Pouštěj **svislé řezy** — jedna
úzká cesta od vstupu k výstupu, pak další.

---

## 14. Návrhový list pro nového agenta

Vyplň dřív, než napíšeš první kód. Když nejde vyplnit, agent není
promyšlený.

```
NÁZEV:
K ČEMU JE:            jednou větou, konkrétně

VSTUPNÍ KANÁLY:       odkud přijímá podněty
KDO SMÍ:              identity a jejich oprávnění

SCÉNÁŘE:              uzavřený seznam toho, co umí
  S1 …                spouštěč → kroky → výstup
  S2 …
  neznámý záměr →     dotaz na člověka

ROLE MODELU:          přesně které kroky, nic víc
  □ rozpoznání záměru
  □ extrakce struktury
  □ syntéza textu
DETERMINISTICKÉ:      všechno ostatní, vyjmenovat

BRÁNY:
  akce               vratnost        režim
  ───────────────────────────────────────────
  …                  …               auto / limit / schválení

KŘÍŽOVÁ KONTROLA:     kde se ověřuje dvěma zdroji
LIMITY:               částky, počty, frekvence

PAMĚŤ:
  trvalá:             osobnost, pravidla
  faktická:           co se ukládá do DB
  co se NEUKLÁDÁ:     citlivé údaje

PROAKTIVITA:          kdy se ozve sám
SELHÁNÍ:              kdo se dozví a jak
VYPÍNAČ:              jak se zastaví

MODULY:               M1 … Mn s kontrakty
POŘADÍ STAVBY:        co první, co blokuje co
```

---

## 15. Antivzory

| Antivzor | Proč je špatný |
|---|---|
| **Agent s volným přístupem ke všem nástrojům** | rozhoduje, na co nemá kontext; tichá větev selhání |
| **AI tam, kde stačí `if`** | drahé, pomalé, nespolehlivé |
| **Důvěra místo vratnosti** | „modelu věřím" není bezpečnostní opatření |
| **Identita podle jména v textu** | kdokoli se za kohokoli vydá |
| **Celá paměť do promptu** | náklady i chybovost rostou s časem |
| **Tiché selhání** | nefunkční agent vypadá jako funkční |
| **Neznámý výsledek zapsaný jako úspěch** | ztracená odpověď se schová do `ok`; škoda se pozná až u protistrany |
| **Automatické přepisování promptů** | rozjede se a nikdo si nevšimne |
| **Integrace před otestováním modulů** | ladíš dvě neznámé naráz |
| **Osobnost napsaná ručně za deset minut** | plochá, obecná, k ničemu |
| **Formulář místo chatu na mobilu** | nepoužije se |

---

## 16. Shrnutí na jednu stránku

1. AI rozpoznává, kód vykonává.
2. Každý konec je vidět: úspěch, selhání, nebo zaznamenaný neznámý výsledek. Tichá větev nesmí existovat.
3. Model dostává jen tři typy úloh: záměr, struktura, text.
4. Osobnost se generuje ze zdrojů, ne píše z hlavy.
5. Identita se váže na kanál, ne na jméno.
6. Režim schvalování určuje vratnost chyby, ne důvěra k modelu.
7. Kde záleží na přesnosti, ověřuj dvěma nezávislými průchody.
8. Chat na mobilu poráží formulář.
9. Agent, který se neozve, když spadne, je horší než žádný.
10. Uč se z vlastních zásahů, ne z metrik. A nikdy automaticky.
11. Moduly s kontrakty, brány, pak teprve integrace.
12. Návrhový list vyplň dřív, než napíšeš první řádek.
