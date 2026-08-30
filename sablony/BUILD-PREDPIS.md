# BUILD PŘEDPIS — od nuly k nasazenému agentovi

Fázový postup, který platí pro libovolného agenta. Konkrétní plán jednoho
projektu vypadá jako [05-html/postup-stavby.html](../05-html/postup-stavby.html);
tenhle dokument je předloha, ze které se takový plán píše.

**Brána** = seznam podmínek na konci fáze. Dokud neplatí všechny, další fáze
se nezačíná. Každá brána zachytává jednu třídu chyb, na kterou by následující
fáze jinak narazila — a to dráž.

| | |
|---|---|
| **Vstup** | nápad na agenta a člověk, který ho bude vlastnit |
| **Výstup** | agent v provozu, s runbookem, evaly a vypínačem |
| **Kritická cesta** | F0 → F1 → F3 → F5 |
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

**Brána**

- [ ] S1 projde od začátku do konce s ručním vstupem
- [ ] Když se něco nepovede, proces **spadne s hlášením** — ne potichu
- [ ] Existují jen dva konce: selhalo a víš o tom, nebo dopadlo dobře
- [ ] Opakovaný běh nedělá věc dvakrát (idempotence u nevratných kroků)

---

## F4 — Model na svoje tři úlohy

**Cíl:** doplnit rozpoznání záměru, extrakci struktury a syntézu textu.
Nic jiného.

- Prompt do `prompts/`, verzovaný jako kód, s číslem verze v zápisu běhu
- Osobnost vygenerovat ze zdrojového materiálu a opravit, nepsat z hlavy
- Naplnit [evaly](kostra-agenta/evals/) — 20–40 reálných vstupů
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

**Brána**

- [ ] Evaly běží v CI a jsou nad prahem (klasifikace 90 %+, extrakce po polích)
- [ ] Změna promptu bez běhu evalů neprojde
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

**Brána**

- [ ] Nevratná akce nad limit nejde provést bez schválení člověkem
- [ ] Vydávání se za jiného uživatele je ošetřené na úrovni kanálu
- [ ] Brána bez odpovědi do X hodin má definované chování
- [ ] Odchozí komunikace nese označení, že ji psala AI

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

- [ ] Agent se zastaví jedním úkonem a ověřil jsi to
- [ ] Simulovaný pád procesu dorazí vlastníkovi do minut
- [ ] Ticho agenta je rozeznatelné od „nebylo co dělat"
- [ ] Obnova ze zálohy je aspoň jednou nanečisto vyzkoušená

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

Předpis je maximum. U jednoduchého agenta pro sebe sama zůstávají povinné
**F0, F1, F3, F6** — návrh, ověření jádra na reálných datech, deterministická
páteř a vypínač. Zbytek se dá zeštíhlit:

| Fáze | Zeštíhlení |
|---|---|
| F2 | plochá struktura místo kostry, kontrakty stačí v hlavě u 1–2 modulů |
| F4 | evaly ručně v deseti případech místo CI |
| F5 | jeden globální limit místo tabulky režimů |
| F7 | bez commit hashe, ale pořád s ruční kontrolou prvního týdne |

Co se přeskočit **nedá nikdy**: reálný vzorek v F1, dva konce procesu v F3
a vypínač v F6. Tohle jsou ty tři věci, jejichž chybějící verze se pozná
až podle škody.
