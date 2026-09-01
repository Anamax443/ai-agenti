# BUILD PŘEDPIS — od nuly k nasazenému agentovi

Fázový postup, který platí pro libovolného agenta. Konkrétní plán jednoho
projektu vypadá jako [05-html/postup-stavby.html](../05-html/postup-stavby.html);
tenhle dokument je předloha, ze které se takový plán píše.

Měření hotového agenta proti tomuhle předpisu popisuje [MERENI.md](MERENI.md);
prázdný formulář se generuje příkazem `python kontrola/brany.py --protokol <verze>`.

**Brána** = seznam podmínek na konci fáze. Dokud neplatí všechny, další fáze
se nezačíná. Každá brána zachytává jednu třídu chyb, na kterou by následující
fáze jinak narazila — a to dráž.

| | |
|---|---|
| **Vstup** | nápad na agenta a člověk, který ho bude vlastnit |
| **Výstup** | agent v provozu, s runbookem, evaly a vypínačem |
| **Kritická cesta** | F0 → F1 → F3 → F6 |
| **Kde se to nejčastěji zvrtne** | přeskočení F1 a F3 — model se pustí dřív, než existuje proces |

---

## F0 — Návrh na papíře

**Cíl:** vědět, co se staví, dřív než vznikne první soubor.

- Vyplnit [návrhový list](navrhovy-list.md) — celý, ne jen hezké části
- Uzavřít seznam scénářů. Co v něm není, agent neumí a neimprovizuje
- Rozdělit kroky na *model* / *kód*. Když si u kroku nejsi jistý, je to kód
- Vypsat moduly a jejich kontrakty (vstup → výstup)

**Brána**

- [ ] Scénáře jsou vyplněné a je jich konečný počet
- [ ] U každého kroku je napsáno, jestli ho dělá model, nebo kód
- [ ] Každá nevratná akce má v tabulce Brány svůj režim
- [ ] **Přísnost (N/Z/V) je odvozená z odpovědí v návrhovém listu**, ne odhadnutá —
      a je napsané, co z ní plyne (viz [principy §7](../01-principy/PRINCIPY-stavby-agentu.md))
- [ ] Je jasné, **kdy je agent hotový** — měřitelně, ne „až bude fungovat"

> Nejde-li vyplnit sekce Scénáře, agent není promyšlený. To není důvod
> začít kódovat a doplnit to potom. To je důvod nezačínat.

**Jak pozná uživatel, co agent umí?** Textové rozhraní nemá tlačítka ani menu.
Uživatel netuší, co si smí říct, a hádá — a když se netrefí, dostane odmítnutí
bez vysvětlení. Agent to musí říct sám: při prvním kontaktu a znovu pokaždé,
když něco odmítne („tohle neumím; umím A, B, C"). Bez toho zůstane půlka
funkcí nepoužitá a uživatel má pocit, že to nefunguje.

---

## F1 — Ověření jádra na reálném vzorku

**Cíl:** změřit nejrizikovější krok dřív, než se kolem něj cokoliv postaví.

Nejrizikovější krok je ten, který nejspíš nevyjde: rozpoznání záměru
z ošklivého vstupu, extrakce z nekvalitního skenu, dohledání v cizím API.
Postav z něj nejmenší možný průchod a pusť ho na **skutečných datech**.

Měř tři věci, každou číslem:

| Veličina | Jak |
|---|---|
| **Přesnost** | na ručně opsané pravdě, ne od oka |
| **Cena** | za jeden průchod × očekávaný objem za měsíc |
| **Čas** | na plné velikosti vstupu, ne na výřezu |

**Brána**

- [ ] Jádro proběhlo na **reálném vzorku**, ne na syntetickém ani zkráceném
- [ ] Přesnost, cena i čas jsou zapsané jako čísla v `NAVRH.md`
- [ ] Když jsou čísla mimo, projekt se **zastavuje nebo mění zadání** — ne pokračuje

> Krátký a syntetický vzorek systematicky lže ve tvůj prospěch. U přepisovače
> vyšel odhad z 70sekundové ukázky na 1,22× délky, skutečnost na hodinovém
> pořadu byla 1,81× — reálná řeč se rozpadla na 1 295 segmentů místo 15
> a každý stojí režii navíc. Rozdíl mezi 68 a 101 minutami běhu.
> Stejně lže vzorek u přesnosti: čisté doklady vypadají skvěle, dokud
> nepřijde vyfocená pomačkaná účtenka.

---

## F2 — Kostra a kontrakty

**Cíl:** místo, kam se dá stavět, a hranice mezi moduly.

- Zkopírovat [kostru agenta](kostra-agenta/) a přejmenovat
- Zafixovat kontrakty modulů. Modul nesahá do cizí databáze — dostane parametr
- Každý modul má CLI a jde spustit bez zbytku systému
- Testovací prostředí **nemá odesílací kanály** — konfigurací, ne přes `if`

**Brána**

- [ ] `NAVRH.md` je v repozitáři vyplněný, ne prázdná šablona
- [ ] Každý modul jde spustit samostatně z příkazové řádky
- [ ] V testovacím prostředí není fyzicky možné odeslat e-mail ani platbu
- [ ] Volání nástrojů jde v testu vypnout **konfigurací** (u API je to parametr
      `tool_choice: none`), ne podmínkou v kódu
- [ ] Žádné tajemství v gitu, jen `*.example`

---

## F3 — Deterministická páteř, ještě bez modelu

**Cíl:** proces, který celý doběhne, aniž by se zeptal modelu.

Vezmi scénář S1 a projeď ho koncem konců s **ručně napsaným vstupem** —
takovým, jaký by jinak vyrobil model. Tohle je ta část, která nese následky:
zápis do databáze, platba, odeslání. Musí být hotová a otestovaná dřív,
než k ní model dostane přístup.

**Pozorovatelný konec se prokazuje vyvoláním, ne tvrzením.** Unit testy nad čistými
funkcemi sem nedosáhnou: vada nebývá v kroku, ale v orchestraci kolem něj. Doložený případ — u JobWatche
neodhalilo 159 testů, 15 kontrol regionu ani 26 evalů čtyři vady naráz: selhání všech zdrojů
skončilo zeleným během, neodeslaná notifikace se už nikdy nezopakovala, dva souběžné běhy si
přepsaly stop příznak a zastavený běh se v historii tvářil jako úspěšný.

**Vyjmenuj stavy a povolené přechody.** „Pozorovatelný konec" je tvrzení o výsledku;
stavový model je **artefakt, na kterém se to dá ověřit**. Bez něj se nedá říct, co je konec:
`ok = 1` zapsané závěrečným krokem je zápis, ne doběhnutí.

Pravidlo, ze kterého plyne zbytek: **nevratná akce leží vždy na přechodu, ne uvnitř stavu.**
Odeslání, platba, zápis do cizího systému nejsou stavy — jsou to hrany mezi nimi. Jakmile je
takhle nakreslíš, musíš odpovědět na otázku, která se jinak přehlédne: *co když přechod selže
uprostřed?*

| Otázka, kterou stavový model zodpoví | Čemu předchází |
|---|---|
| Kde leží stav mezi „zapsáno" a „odesláno"? | skóre uložené, zpráva neodeslaná — a fronta se k ní nikdy nevrátí |
| Kdo vlastní běh a co smí druhý běh? | dva souběžné běhy si přepíšou stav; druhý smaže stop příznak prvního |
| Které stavy jsou terminální? | zastavený běh, který závěrečný zápis přepíše na úspěšný |
| Co se stane s neznámým výsledkem? | volání proběhlo, odpověď se ztratila — a nikdo neví, jestli opakovat |

Všechny čtyři sloupce vpravo jsou doložené vady jednoho jediného agenta. Nevznikly
z nepozornosti: **každá z těch funkcí se chová správně sama o sobě.** Vada je ve vztahu
mezi nimi, a ten je vidět teprve na diagramu.

Vzory na to existují — outbox, lease, idempotency key, fronta pro nedoručitelné. Předpis je
**nepředepisuje**: kód sem nepatří a vzor vázaný na jazyk a platformu zastará dřív než
otázka. Předepisuje odpovědi na ty čtyři otázky. Kdo je zná, vzor si najde; kdo je nezná,
vzor beztak použije špatně.

**Brána**

- [ ] S1 projde od začátku do konce s ručním vstupem
- [ ] Má-li agent aspoň jednu nevratnou akci: **stavy a povolené přechody jsou vyjmenované**
      v návrhovém listu a **každá nevratná akce leží na přechodu**, ne uvnitř stavu
- [ ] U každého přechodu s nevratnou akcí je napsané, **co se stane, když selže uprostřed**
- [ ] Když se něco nepovede, proces **spadne s hlášením** — ne potichu
- [ ] Každý konec je **pozorovatelný**: známý úspěch, známé selhání, nebo zaznamenaný
      neznámý výsledek — žádná tichá větev
- [ ] Neznámý výsledek (volání proběhlo, odpověď se ztratila) má vlastní stav a další
      krok: dotaz na cílový systém, idempotentní opakování, nebo fronta pro člověka.
      Nikdy opakování naslepo a nikdy zápis `ok`
- [ ] Opakovaný běh nedělá věc dvakrát (idempotence u nevratných kroků)
- [ ] Každý konec je **vyvolaný acceptance testem**, ne jen popsaný: všechny zdroje dolů ·
      selhání po zápisu a před odesláním · **timeout po odeslání a před zápisem** ·
      dva souběžné běhy · zastavení uprostřed
- [ ] Dva běhy si nemůžou přepsat stav — buď druhý běh nejde spustit, nebo má běh zámek

---

## F4 — Model na svoje tři úlohy

**Cíl:** doplnit rozpoznání záměru, extrakci struktury a syntézu textu.
Nic jiného.

- Prompt do `prompts/`, verzovaný jako kód, s číslem verze v zápisu běhu
- Osobnost vygenerovat ze zdrojového materiálu a opravit, nepsat z hlavy
- Naplnit [evaly](kostra-agenta/evals/) — 20–40 reálných vstupů, **včetně těžkých záporů**
- Kde záleží na číslech, zapojit křížovou kontrolu dvěma nezávislými průchody

**Metriky, které u agenta dávají smysl.** „Prošlo / neprošlo" je málo — potřebuješ
vědět, *co* se pokazilo:

| Metrika | Co měří | Co znamená nízká hodnota |
|---|---|---|
| **tool recall** | zavolal všechny kroky, které měl? | krok vynechal |
| **tool precision** | nezavolal navíc něco zbytečného? | špatně pochopil záměr |
| **parameter accuracy** | předal správné argumenty? | správná akce, špatné číslo |
| **phrase recall** | obsahuje výstup, co obsahovat musí? | chybí povinná formulace |
| **task success** | dopadl celý scénář? | souhrn všeho výše |

Rozdíl mezi „zavolal špatný nástroj" a „zavolal správný nástroj se špatnou
částkou" je rozdíl mezi zmatením a škodou. Jedno číslo ti ho neřekne.
U extrakce hodnoť pole po poli, ne celý výstup jako jeden test.

**Sada bez těžkých záporů měří jen sama sebe.** Zápor, který zahodí deterministický filtr,
o modelu nevypovídá — model ho nikdy neuvidí. Cenu má jen zápor, který filtrem projde
a odmítnout ho musí model. Doložený případ: JobWatch má 17 záporných případů a všech 17
odmítne prefiltr, takže deklarovaná precision 100 % o schopnosti rozlišovat neříká nic.

**Brána**

- [ ] Evaly jsou nad prahem (klasifikace 90 %+, extrakce po polích) a **měří tu příčku, která
      rozhoduje v produkci**: je-li backend dostupný z CI, běží v CI; existuje-li jen za běhu
      (binding, tajemství jen v produkci), měří se na nasazené verzi, ručně, s protokolem,
      a v běhu je zapsané, která příčka odpověděla. Dokud takový eval neproběhl, je nasazení
      **kandidát**, ne schválená verze
- [ ] Sada obsahuje **záporné případy, které projdou deterministickým filtrem** — jinak neměří
      schopnost modelu odmítnout
- [ ] Změna promptu bez běhu evalů neprojde — brána hlídá **běh evalů**, ne jen zvýšení verze
- [ ] Cizí text je ohraničený a označený za nedůvěryhodná data **na každém volání modelu**,
      ne jen na tom hlavním — a nejdřív tam, kde má model nástroje
- [ ] Model nemá přístup k žádné nevratné akci napřímo — jen přes proces z F3
- [ ] Nepřátelský vstup neposune agenta mimo scénář (viz návrhový list)
- [ ] U sporných výstupů vrací model **vlastní míru jistoty** a pod prahem se ptá
- [ ] Podíl případů, které padnou na člověka, drží pod ~10 % — nad tím člověk
      otupí a začne odklikávat

---

## F5 — Brány, limity, identita

**Cíl:** ohraničit, co agent smí sám.

- Režim u každé akce podle **vratnosti chyby**, ne podle důvěry k modelu
- Limity: částky, počty, frekvence — a co se stane při překročení
- Identita z kanálu (číslo, ID, podpis webhooku), nikdy ze jména v textu
- Agent se přiznává, že je AI, když píše ven — vyžaduje to i AI Act

**Princip nejmenší moci.** Nástroj je úzce vymezená operace
(`vystav_doklad(id)`), ne obecná brána (`spust_sql(dotaz)`). Doložený případ:
agent dostal přístup k databázi, „optimalizoval výkon" a smazal půlku řádků
produkční tabulky. Model si nemá co skládat dotazy — dostane tlačítka, ne klávesnici.

**Autonomie roste, nezačíná nahoře.** Role člověka se posouvá
*vykonavatel → kontrolor → spolupracovník → správce* a s ní i to, co agent smí sám.
Nový agent nejdřív připraví návrh, teprve po čase ho odesílá. Opačný postup se
trestá: Klarna v roce 2024 nahradila kolem 700 lidí v podpoře chatbotem, objem
stížností vyletěl a v roce 2025 nabírala lidi zpět. Stejně důležitá je cesta
zpátky — způsob, jak agentovi pravomoc odebrat, když se ukáže, že na ni nemá.

**Odchozí identita: známý kanál, vlastní klíč.** Odpovídat se musí z kanálu, který
protistrana zná — z jiné adresy se rozpadne vlákno i doručitelnost. Z toho ale neplyne, že
agent má držet **tvoje** přihlašovací údaje. Dostane vlastní, s nejmenším potřebným
rozsahem a **samostatně zneplatnitelný**: vypnutí agenta pak je jeden úkon, ne změna hesla
vlastníka. Ke každé odchozí zprávě patří dohledatelná značka (hlavička, ID případu) a kopie
navázaná na případ.

**Čí jsou data v tom kanálu?** Předpis dlouho mlčky předpokládal, že vlastník agenta je
i vlastníkem dat. U firemní schránky to neplatí: agent z ní píše **jménem firmy** a čte
cizí data, která navíc posílá do modelu třetí strany. To není rozhodnutí vlastníka agenta.
Když se vlastník dat a vlastník agenta liší, musí být zapsané **kdo dal souhlas a v jakém
rozsahu** — jinak se ta otázka nikdy nepoloží, protože technicky nic nebrání.

**Brána**

- [ ] Nevratná akce nad limit nejde provést bez schválení člověkem
- [ ] Vydávání se za jiného uživatele je ošetřené na úrovni kanálu
- [ ] Brána bez odpovědi do X hodin má definované chování
- [ ] Odchozí komunikace odcházející **bez schválení člověkem** nese označení, že ji psala
      AI. U schválené odpovědi nese odpovědnost schvalovatel
- [ ] Agent má na každý odchozí kanál **vlastní přihlašovací údaj**, samostatně
      zneplatnitelný a s nejmenším potřebným rozsahem — ne údaj vlastníka
- [ ] U každého kanálu je uvedený **vlastník dat**; když to není vlastník agenta, je
      zaznamenané, kdo dal souhlas a v jakém rozsahu

---

## F6 — Selhání, runbook, vypínač

**Cíl:** aby se rozbitý agent poznal a dal zastavit.

- Vyplnit [runbook](kostra-agenta/runbook.md): vypnutí, časté poruchy, obnova
- Hlášení o pádu jde **člověku**, ne jen do logu
- Vypínač = jeden úkon. Vyzkoušený, ne teoretický

**Čtyři způsoby, jak selže dohled člověka.** Jsou popsané a počítá se s nimi:

| Selhání | Jak se projeví |
|---|---|
| **Slepá důvěra v automat** | člověk přestane výstup číst, „zatím to vždycky sedělo" |
| **Únava z hlášení** | důležité upozornění zapadne mezi deseti nedůležitými |
| **Ztráta dovednosti** | po roce automatiky už člověk neumí zasáhnout ručně |
| **Rozejité zájmy** | agent tlačí na rychlost, člověk potřebuje jistotu |

Proto: hlásit málo a adresně. A u každé eskalace dodat kontext — co agent zkusil,
proč to vzdal a co přesně má člověk rozhodnout. Eskalace bez kontextu je jen
přehození práce.

**Brána**

- [ ] Agent se zastaví jedním úkonem a ověřil jsi to **za běhu**, ne na stojícím systému
- [ ] Simulovaný pád procesu dorazí vlastníkovi do minut
- [ ] Ticho agenta je rozeznatelné od „nebylo co dělat"
- [ ] Obnova ze zálohy je aspoň jednou nanečisto vyzkoušená
- [ ] Zastavený běh zůstane zastavený: závěrečný zápis ho nepřepíše na úspěch a souběžný běh
      mu nesmaže stop příznak

---

## F7 — Nasazení

**Cíl:** provoz, u kterého je vidět, co běží.

- Do buildu commit hash, ať je poznat běžící verze
- Pozorovatelnost: kolik průchodů, kolik selhání, kolik stálo
- **První týden každý výstup ručně zkontroluj** dřív, než odejde ven
- Novou verzi pusť napřed **naslepo vedle ostré** — stejné vstupy, výstup se
  zahodí a jen porovná. Teprve pak na malý podíl provozu

**Chyba, nebo rozptyl?** Model je pravděpodobnostní, takže odlišný výstup ještě
není porucha. Pravidlo: pusť tentýž vstup **3–5×**. Selže-li nad 80 % běhů, je to
systematická chyba a jde do opravy. Selže-li jednou ze čtyř, je to rozptyl —
zaloguj a sleduj trend. Bez tohohle pravidla se buď honí duchové, nebo se
přehlédne skutečná regrese.

**Brána**

- [ ] Na nasazení je vidět verze a datum
- [ ] Náklady za týden provozu odpovídají odhadu z F1 (±rozumně)
- [ ] Ruční kontrola prvního týdne nenašla nic, co by šlo tiše ven

---

## F8 — Provoz a růst

**Cíl:** aby se agent zlepšoval, ale ne sám od sebe.

- Každá chyba v provozu → nový případ do evalů. Po roce máš materiál, který
  se nedá koupit
- **Ukládej i povedené průchody**, nejen selhání — z nich vznikne referenční
  „zlatá cesta", proti které se pozná regrese
- Uč se z vlastních zásahů, ne z metrik
- Prompt se **nikdy nepřepisuje automaticky**
- Každá změna promptu nebo nástroje má zapsané: co se pozorovalo, co se změnilo,
  jak se pozná, že to pomohlo

**Agent málokdy spadne — spíš tiše zhorší.** Proto sleduj i posun rozdělení, ne
jen chybovost. Nejlevnější měřítko: podíly kategorií (které scénáře se spouštějí,
které nástroje se volají) proti výchozímu týdnu.
Rozdíl **pod 0,1 klid · 0,1–0,25 sleduj · nad 0,25 zasáhni** (index PSI).
K tomu implicitní signály od lidí: jak často se ptají znovu jinými slovy a jak
často to vzdají uprostřed. Obojí přijde dřív než stížnost.

**Brána (opakovaně, ne jednorázově)**

- [ ] Evalů přibývá s provozem
- [ ] Změny promptu mají review jako změny kódu
- [ ] Jednou za čas: sedí ještě seznam scénářů, nebo se agent někam rozlezl?

---

## Co u malého agenta přeskočit

Předpis je maximum. **Zeštíhlit ale nesmíš podle toho, jak malý ti agent připadá.**
Rozhoduje dvojice odpovědí z návrhového listu:

> Zjednodušit smíš, jen když platí **obojí**:
> 1. přísnost je **N** (osa systému, [principy §7](../01-principy/PRINCIPY-stavby-agentu.md)),
> 2. žádná akce agenta není nevratná reputačně ani fyzicky (osa akce).
>
> Platí-li jen jedno, zjednodušit lze všechno **kromě F4 a F5**.
> Neplatí-li ani jedno, předpis platí celý.

Tohle nahrazuje dřívější „u jednoduchého agenta pro sebe sama". Ta kategorie byla
subjektivní a rozhodoval o ní ten, kdo měl na zjednodušení zájem — každý autor svého
agenta zná a považuje ho za jednoduchý, protože zná jeho **záměr**. Vratnost a dopad
záměr neznají, jen následek.

Při přísnosti N zůstávají povinné **F0, F1, F3, F6** — návrh, ověření jádra na reálných
datech, deterministická páteř a vypínač. Zbytek se dá zeštíhlit:

| Fáze | Zeštíhlení |
|---|---|
| F2 | plochá struktura místo kostry, kontrakty stačí v hlavě u 1–2 modulů |
| F4 | evaly ručně v deseti případech místo CI |
| F5 | jeden globální limit místo tabulky režimů |
| F7 | bez commit hashe, ale pořád s ruční kontrolou prvního týdne |

Co se přeskočit **nedá nikdy**: reálný vzorek v F1, pozorovatelný konec procesu v F3
a vypínač v F6. Tohle jsou ty tři věci, jejichž chybějící verze se pozná
až podle škody.
