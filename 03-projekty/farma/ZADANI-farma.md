# ZADÁNÍ — Farma AI agentů (osobní dispečer)

> 🇨🇿 Čeština · [🇬🇧 English](ZADANI-farma.en.md)

**Stav: F0, na papíře. Nepostaveno, a záměrně se zatím stavět nemá.**
Tenhle list je návrhový artefakt, ne dokumentace běžící věci. Vznikl 1. 9. 2026 z rozboru
vizuálního náčrtu a z rozhodnutí, která k němu padla. Slouží k tomu, aby se dalo pokračovat
odjinud.

---

## 1. Co to má být

Jeden hlavní agent (orchestrátor) rozpozná agendu, předá ji specialistovi a drží rozehraný
případ, dokud není dokončený — i když se na odpověď čeká několik dní.

| Vrstva | Obsah |
|---|---|
| **Vstupy** | Telegram · Seznam + Gmail · Google Kalendář · OneDrive + Synology · časovače |
| **Vstupní robot** | přijme zprávu, uloží originál, přidělí CASE-ID, obnoví rozpracovaný případ |
| **Orchestrátor** | rozpozná agendu, vybere specialistu, propojí víc agend u složeného úkolu |
| **Specialisté** | hledání práce · doklady a archiv · schůzky a zakázky · e-mail · finance a Fio · analýzy |
| **Společné služby** | stavy případů (`new · waiting · snoozed · approved · done · unknown`) · pravidla a oprávnění · registr agentů · sdílená paměť · úložiště · dohled a audit |
| **Výstupy** | člověk v Telegramu · Seznam/Gmail · Kalendář · Fio banka |

Každý specialista má v náčrtu kontrakt `Dostane / Vrátí / **Nesmí**`.

## 2. Co na návrhu obstálo

Měřeno proti [build předpisu](../../sablony/BUILD-PREDPIS.md), ne obecně:

- **Orchestrátor sám úkol neřeší** — přidělí CASE-ID a vybere specialistu. Jádro („AI
  rozpoznává, kód vykonává") aplikované na nejvyšší úrovni, kde se obvykle poruší první.
- **Robotická vrstva je nakreslená zvlášť** od agentů. Dělba práce není v hlavě.
- **Stavy případu obsahují `unknown`** — a to je věc, kterou předpis dostal teprve
  1. 9. 2026 (nález `N9`, tři stavy místo dvou). Návrh ji má sám od sebe.
- **„Nejasnost se nepřikrášluje"** — „30. 6." bez roku se musí dojasnit, agent datum nesmí
  domyslet. To je požadavek F4 na míru jistoty a dotaz pod prahem.
- **Kontrakty s negativním vymezením** (`Nesmí`) — víc, než žádá F2.
- **Ve `Nesmí` u financí stojí** „autorizovat dávku ve Fio" a „zopakovat platbu při neznámém
  výsledku". Druhá půlka je učebnicově správně a předjímá `N9`.

## 3. Nálezy proti návrhu

Očíslované, aby se na ně dalo odkazovat. Seřazené podle závažnosti.

### FA1 — Seznam scénářů není uzavřený a být nemůže

F0 žádá konečný počet scénářů. Šest agend × podagendy × „složený úkol přes více agend" je
kombinatorický prostor, a agenda *Analýzy a znalosti — hledá napříč agendami* je neohraničená
ze své podstaty.

**Tohle je nejzávažnější nález.** Metodika stojí na uzavřeném seznamu; tenhle návrh ho nemá.
Buď se rozsah zúží, nebo se přizná, že jde o jiný typ agenta, než pro jaký předpis platí
(souvisí s nálezem `A2` — rozsah platnosti etalonu).

### FA2 — Přísnost je V, ne N

Podle [osy systému](../../01-principy/PRINCIPY-stavby-agentu.md): cizí text od cizích lidí
(e-mail), platby (Fio), komunikace ven třetím stranám, osobní údaje. **Žádné zjednodušení
fází se tady nesmí použít** — a označení „osobní digitální dispečer" k tomu svádí.

### FA3 — Cizí vstup spouští agendu

Příchozí e-mail → vstupní robot → orchestrátor → *vybere a spustí agendu*. Principy §6 říkají:
*„Cizí vstup nikdy nespouští akci přímo. E-mail od neznámého projde rozpoznáním záměru
a skončí v denním přehledu, ne v procesu."*

Útočník tu neovlivňuje výstup — ovlivňuje **routing**. To je třída injection, kterou předpis
pojmenovanou nemá.

### FA4 — Nevratné akce leží na přechodech a návrh o nich mlčí

Stavy případu jsou vyjmenované, ale odeslat e-mail, zapsat do kalendáře a importovat dávku do
Fio jsou **přechody**, ne stavy. Chybí odpověď na otázku *co když přechod selže uprostřed* —
tedy nález `N3` doplněný do F3 1. 9. 2026.

Konkrétní past u e-mailu: SMTP zprávu přijme, lokální zápis se nepovede, agent neví, jestli
odešla. Slepé opakování = cizí člověk dostane tutéž zprávu dvakrát, a to je reputačně nevratná
akce.

**Řešení, které je zdarma:** Message-ID se vygeneruje a uloží **před** odesláním. Při neznámém
výsledku se neopakuje, ale prohledají se Odeslané na to Message-ID. Message-ID je tedy
idempotency key a protokol ho má stejně.

### FA5 — Jedno společné schválení u složeného úkolu

Ve scénáři *Složený úkol* stojí „Jedno společné schválení" pro kalendář + Fio + e-mail.
F5 povoluje dvě brány místo jedné (schválit plán, pak jednotlivé nevratné kroky), ale ne slít
reputačně a finančně nevratnou akci do jednoho kliknutí.

### FA6 — Chybí čísla z F1

U farmy, kde orchestrátor běží na **každý příchozí e-mail**, je cena za průchod × objem ta
nejdůležitější číslice. V návrhu žádná není. F1 žádá přesnost, cenu a čas.

### FA7 — Vrstva bezpečnosti nástrojů

Model má sahat na e-mail, kalendář i banku. Chybí allowlist nástrojů a domén podle kroku,
validace argumentů proti schématu, výstupní kontrola a testy exfiltrace. To je nález `A6`,
o kterém **mlčí i předpis sám** — takže to není porušení, ale díra na obou stranách.

### FA8 — Přístup do schránky je vždycky celá historie

IMAP nedává „novou poštu". Dává **celou schránku** — všechny složky, archiv, Odeslané, Koš,
roky zpátky. Omezení na „jen od dneška" je zdrženlivost klienta (`SEARCH SINCE`), **ne
hranice oprávnění**. Kdo má ten údaj, má všechno.

To je zároveň riziko i příležitost a je potřeba je rozdělit:

**Riziko.** Agent s heslem pro aplikace může přečíst i to, co jsi mu nikdy dát nechtěl —
starou osobní poštu, finanční věci, zdravotní věci — a **posílá to do modelu třetí strany**.
U `maxla@seznam.cz` to zhoršuje už zapsanou výjimku: rozsah nejde omezit ani na protokol,
natož na složku nebo období.

**Omezení proto musí být v kódu, ne v promptu.** Vyjmenované složky a datum „od" jako pevný
filtr před voláním modelu. Doložený důvod je z JobWatche: pravidlo o regionu bylo nejdřív
věta v promptu, slabý model ji ignoroval a pražský inzerát dostal 80/100 s odůvodněním, že
Praha je v preferovaném regionu. **Tvrdá kritéria do promptu nepatří.**

**Příležitost.** Historie je přesně ten **reálný vzorek**, který žádá F1 — a nemusí se na něj
čekat. Místo padesáti nových e-mailů jich jsou tisíce.

**A jde ji použít, aniž bys agenta ke schránce vůbec pustil:** vyexportuj vzorek zpráv do
souboru a změř routing orchestrátoru na něm. F1 se tím splní **dřív**, než vznikne jakýkoli
živý přístup — a když měření dopadne špatně, žádné oprávnění se nikdy nevydávalo. To je
nejlevnější i nejbezpečnější pořadí.

---

## 4. Kanály a schránky

Tři adresy nejsou jedna třída. Rozhodnutí padla 1. 9. 2026.

| Schránka | Čí jsou data | Přísnost | Verdikt |
|---|---|---|---|
| `mtrnka@axima.cz` | **zaměstnavatele** | V | **do farmy nedávat** |
| `maxla@seznam.cz` | vlastníka + cizích pisatelů | Z | **použitelná, s výjimkou** |
| `bass443@gmail.com` | vlastníka + cizích pisatelů | Z | použitelná, čistý případ |

### axima.cz — červená čára

Není to schránka vlastníka agenta. Jsou v ní zákazníci, ceny, interní věci a osobní údaje
kolegů. Agent, který z ní odpovídá, **píše jménem firmy**; agent, který ji jen čte, **posílá
firemní data do modelu třetí strany**. To není rozhodnutí vlastníka agenta a musí být napsané,
kdo ho udělal a v jakém rozsahu.

Prakticky: axima.cz je na O365, takže vlastní údaj agenta znamená registraci aplikace v Entra
a **souhlas správce tenantu** — tedy papírovou stopu. To je spíš výhoda.

**Doporučení: vynechat.** Když ano, tak jen čtení, jen vyjmenované složky, s pravidlem, co se
z ní nesmí dostat do promptu. Rozhodně ne odesílání.

### seznam.cz — ověřeno, použitelné s vědomou výjimkou

Ověřeno v dokumentaci Seznamu 1. 9. 2026:

| Otázka | Odpověď |
|---|---|
| Samostatné heslo odlišné od hesla k účtu? | **ano** — a je vynucené, nesmí být stejné |
| Více hesel, zrušit jedno? | **ne** — jedno jediné, *„nelze smazat, pouze změnit"* |
| Omezit rozsah (jen IMAP / jen SMTP)? | **ne** — jedno heslo = IMAP/POP3 + SMTP + CalDAV |
| Vidět poslední použití? | dokumentace neuvádí — **neověřeno** |
| Vztah k 2FA? | heslo pro aplikace **vyžaduje zapnuté 2FA**; vypnutím 2FA se deaktivuje |

Zdroje: [Poštovní programy a CalDAV při 2FA](https://o-seznam.cz/napoveda/ucet/en/dvoufazove-overeni/postovni-programy/) ·
[Dvoufázové ověření](https://o-seznam.cz/napoveda/ucet/en/dvoufazove-overeni/)

**Co z toho plyne:**

- Agent **nedostane heslo k účtu** → podmínka F5 o vlastním údaji je splnitelná.
- **Vypínač funguje** — změna hesla pro aplikace je jeden úkon a heslo k účtu se nemění.
- **Ale je to jeden sdílený údaj pro všechny klienty schránky.** Před nasazením musí být
  vypsané, kdo další ho používá (telefon, poštovní klient, kalendář) — to jsou vedlejší škody
  vypínače.
- **Rozsah nejde omezit.** Údaj „jen na čtení" umí i odesílat a otevře kalendář přes CalDAV.
  **Vědomá výjimka z principu nejmenší moci**, zapsaná, ne přehlédnutá.

Ověřovací postup na stupeň `U3` (vyvoláno v prostředí):

```bash
# 1. zapnout 2FA na ucet.seznam.cz -> Zabezpečení
# 2. nastavit Heslo pro aplikace (musí být jiné než heslo k účtu)

# 3. heslo K ÚČTU musí po zapnutí 2FA selhat:
curl -sS -u "maxla@seznam.cz" "imaps://imap.seznam.cz:993/" >/dev/null \
  && echo "PRIHLASENI OK" || echo "PRIHLASENI SELHALO"     # očekáváno: SELHALO

# 4. heslo PRO APLIKACE musí projít (týž příkaz)          # očekáváno: OK

# 5. změnit heslo pro aplikace a znovu:
#    staré  -> musí selhat
#    nové   -> musí projít
#    web    -> heslo k účtu se nezměnilo
```

Heslo se nepíše do příkazu — curl si o něj řekne. Jinak skončí v historii shellu a v seznamu
procesů.

### gmail.com — čistý případ

OAuth s omezenými rozsahy (`gmail.send`, `gmail.readonly`), ne heslo pro aplikaci. Vypínač je
odebrání přístupu v účtu Google — jeden úkon, heslo se nemění.

### Pravidlo napříč schránkami

> **Případ nesmí překročit hranici schránky.** Vlákno z axima.cz se nikdy neodpoví z Gmailu,
> obsah z jedné schránky se necituje do odpovědi z druhé, a případ založený v jedné schránce
> v ní zůstane.

Bez toho je jen otázkou času, kdy se firemní vlákno objeví v soukromé odpovědi. To je vada,
která se pozná až u protistrany — nejhorší sloupec v tabulce přísnosti.

### Odchozí identita

Zapracováno do předpisu 1. 9. 2026 (F5): odpovídá se **z kanálu, který protistrana zná**
(jinak se rozpadne vlákno i doručitelnost), ale **pod vlastním, samostatně zneplatnitelným
údajem agenta**. Ke zprávě patří dohledatelná značka v hlavičce (`X-Agent-Case`) a kopie
navázaná na případ. Označení „psala AI" se řídí **režimem schválení**, ne kanálem.

## 5. Škálování modelů

Směr: farmy poběží na **různých modelech, ne vždy na tom nejchytřejším**. Pravidla, která
z toho plynou a zatím **nejsou v předpisu**:

- **Příčka se volí per krok, ne per agent.** Levný model na roztřídění do šesti přihrádek,
  drahý na sporná procenta. Kdo je drahý potřebuje, rozhoduje **kód**.
- **„Stačí levnější" se neříká, měří se** — na eval sadě téhož kroku. Jinak se z opatrnosti
  používá drahý všude a farma je neufinancovatelná.
- **Eskalace na vyšší příčku je viditelná událost** a její podíl je metrika.
- **V každém běhu je zapsané, která příčka odpověděla** (to už v F4 je).

Doložený precedens z JobWatche: **free model recall 50 %, placený 83 %** — a sada dvakrát
měřila jinou příčku, než která rozhodovala v produkci. U farmy se šesti agendami a třemi
příčkami je ta past šestkrát větší.

## 6. Schéma se generuje, nekreslí

Požadavek: výstupem má být HTML schéma jako v n8n, aby bylo vidět, **ve které fázi to
kolabuje**.

Ručně kreslené schéma je dokumentace záměru a za tři měsíce ukazuje něco jiného, než co běží —
je to fajfka, co přežila nález, jen v grafické podobě. Aby ukazovalo, kde to padá, musí se
**generovat ze dvou zdrojů**:

| Zdroj | Co dodá |
|---|---|
| stavový model | uzly a hrany, tedy co je deklarované |
| záznamy běhů | kolik případů tudy prošlo, kolik uvázlo, čas, cena, **která příčka odpověděla** |

A nejcennější je **rozdíl mezi nimi**: hrana, která je v deklaraci a v provozu se nepoužila;
přechod, který v deklaraci není a v datech se objevuje. To jsou nálezy.

**Musí být po hranách, ne po uzlech.** Doložený důvod: všechny čtyři orchestrační vady
JobWatche byly na hranách mezi správně fungujícími funkcemi.

Generátor je **kód**, takže do `ai-agenti` nepatří ([AGENTS.md](../../AGENTS.md)). Má vzniknout
v projektu — nejlevněji v JobWatchi, kde už data jsou (`promptVersion`, statistika providerů,
stavy běhů).

## 7. Co dál

Pořadí je vědomé a plyne z předpisu, ne z chuti stavět.

1. **F1 na nejrizikovějším kroku, a tím není žádný ze šesti agentů.** Je to **routing
   orchestrátoru na nepřátelském vstupu**. Padesát reálných e-mailů: kolikrát vybere správnou
   agendu a kolik z nich ho přesměruje schválně napsaná zpráva. Jedno odpoledne, a rozhodne
   o celém návrhu.
2. **Jedna agenda celá, ne šest napůl.** Hodnota návrhu není v šesti agentech, ale ve sdílené
   paměti případů, CASE-ID a stavech. To se dá ověřit na jedné.
3. **Vejde se JobWatch do farmy jako agenda číslo jedna?** Běží, má rok incidentů, vypínač,
   evaly a od 1. 9. 2026 zavřenou injection díru na všech třech cestách volání modelu. Otázka
   pro F0 nezní „jak postavit agendu hledání práce", ale jestli si ta dvě zadání neodporují.
   Když ano, je to nález proti farmě — a je levnější ho najít teď.

## 8. Otevřené otázky

| # | Otázka | Blokuje |
|---|---|---|
| **OA1** | Zúžit rozsah farmy na uzavřený seznam scénářů, nebo přiznat jiný typ agenta? | `FA1`, a tím i F0 |
| **OA2** | Smí orchestrátor vybírat agendu z cizího e-mailu, nebo musí cizí vstup skončit v denním přehledu? | `FA3` |
| **OA3** | Kdo další používá heslo pro aplikace u `maxla@seznam.cz`? | nasazení Seznamu |
| **OA4** | Zůstává axima.cz mimo, nebo se žádá souhlas? Kdo ho dá a v jakém rozsahu? | `FA2`, F5 |
| **OA5** | Kde vznikne generátor schématu — v JobWatchi jako první případ? | kapitola 6 |
