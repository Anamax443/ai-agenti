# Zdroje

Odkud metodika v `01-principy/` pochází a jak si to ověřit.

---

## Hlavní zdroj — rozhovor s Markem Bartošem

**Keci a politika**, speciál „Umělá inteligence je naše UFO".
Hosté: Marek Bartoš (popularizátor vědy a AI). Moderují Bohumil Pečinka
a Petros Michopulos. Volně dostupná je jen první polovina pořadu,
druhá je za předplatným (keciapolitika.cz, herohero.co).

### Jak vznikl přepis

Lokálně přes [mp3totxt](https://github.com/Anamax443/mp3totxt) 0.1.0
(faster-whisper, model `medium`, jazyk `cs`, bez GPU):

| Údaj | Hodnota |
|---|---|
| Délka audia | 3 351 s (55:51) |
| Doba přepisu | 6 076 s (1:41:16) |
| Poměr | **1,81×** délky audia |

### Co s přepisem v repozitáři není

Přepis (`.txt`, `.json`, `.srt`, `.vtt`) leží v `00-zdroje/prepisy/`
**jen lokálně** — složka je v `.gitignore`. Repozitář je veřejný a přepis
cizího pořadu, jehož druhá polovina je placená, do něj nepatří.
Do repozitáře jde jen tenhle rozbor: časy, parafráze a krátké citace.

### Omezení, se kterými počítej

- Přepis pokrývá **jen první polovinu** pořadu (volně dostupnou část).
- Model `medium` komolí vlastní jména a méně častá slova. „Skippy" se
  v přepisu střídá jako *skipy / Skypy / Stiffy*, „Perplexity" jako
  *Pelprexity*, „arXiv/bioRxiv" jako *ArcSive / BioXSive*, „Anthropic"
  místy zmizí. **Nikdy z přepisu necituj jméno nebo číslo bez poslechu.**
- Časy v tabulce níže jsou z `.json` (pole `start`), ne z audia ručně.

---

## Mapa: co v pořadu zaznělo a kde se to v repu projevilo

| Čas | Co zaznělo | Kde to je |
|---|---|---|
| 13:25 | Jedna hlavní mysl drží vzpomínky, výkon dělají menší levnější části; do každé je „infuzovaná trocha osobnosti" | [Anatomie agenta](../01-principy/PRINCIPY-stavby-agentu.md#3-anatomie-agenta) |
| 11:43 | Osobnost vytažená z literární předlohy (Skippy Velkolepý, *The Expeditionary Force*) přes analýzu e-booků | [Osobnost jako artefakt](../01-principy/PRINCIPY-stavby-agentu.md#4-osobnost-jako-artefakt) |
| 17:02 | Limit 50 000 Kč; u předschválených dodavatelů platí bez schvalování a jen informuje | [Brány](../01-principy/PRINCIPY-stavby-agentu.md#7-brány-kdy-se-ptát-člověka) |
| 17:29 | **„Nebojím se, protože ona to ve skutečnosti nedělá umělá inteligence."** | [Základní princip](../01-principy/PRINCIPY-stavby-agentu.md#1-základní-princip) |
| 18:59 | Fakturu přepíše Mistral OCR a nezávisle Gemini; shodnou se → jede dál, neshodnou → dotaz na člověka. Přepsat, ne zaplatit. | [Křížová kontrola](../01-principy/PRINCIPY-stavby-agentu.md#8-křížová-kontrola) |
| 19:45 | „Skippy to vlastně neplatí" — jen rozpozná a pošle do procesu, platbu dělá mechanika | [Základní princip](../01-principy/PRINCIPY-stavby-agentu.md#1-základní-princip) |
| 20:53 | Předem definovaný proces má **jen dva konce**: selže s hlášením, nebo dopadne dobře | [Selhání a pozorovatelnost](../01-principy/PRINCIPY-stavby-agentu.md#11-selhání-a-pozorovatelnost) |
| 21:16 | Důvěra nevznikla časem — přišla hned, protože nestojí na AI, ale na kódu „co jede na tvrdo" | [Brány](../01-principy/PRINCIPY-stavby-agentu.md#7-brány-kdy-se-ptát-člověka) |
| 21:32 | Analogie s QR kódem: nedůvěřuješ modelu, důvěřuješ procesu s nízkou chybovostí | tamtéž |
| 26:44 | Poloha každých 5 minut → z rychlosti pozná, že řídí, a pošle hlasovku místo textu | [Vstupy a periferie](../01-principy/PRINCIPY-stavby-agentu.md#5-vstupy-a-periferie) |
| 28:34 | Manželka má u agenta **větší práva** než majitel (může přeskládat kalendář) | [Oprávnění a identita](../01-principy/PRINCIPY-stavby-agentu.md#6-oprávnění-a-identita) |
| 29:14 | Ověření identity přes WhatsApp: telefonní číslo + další identifikátory, ne jméno v promptu | tamtéž |
| 30:50 | Ranní report: agent přečte e-maily a shrne, kdo co chce | [Proaktivita](../01-principy/PRINCIPY-stavby-agentu.md#10-proaktivita) |
| 31:48 | Agent se **vždy přizná, že je AI** — odkaz na AI Act | [Oprávnění a identita](../01-principy/PRINCIPY-stavby-agentu.md#6-oprávnění-a-identita) |
| 34:36 | Náklady: ~5 000 Kč/měs provoz + ~2 000 Kč/měs další vývoj | [Proč na tom záleží ekonomicky](../01-principy/PRINCIPY-stavby-agentu.md#proč-na-tom-záleží-ekonomicky) |
| 36:08 | **Proces stojí pár centů na fakturu, totéž přes AI stojí dolary**; kdyby vše dělala AI, běželo by to na desítky tisíc měsíčně | tamtéž |
| 37:12 | Agent si sám čte arXiv/bioRxiv a hledá, jak se zlepšit | [Zlepšování](../01-principy/PRINCIPY-stavby-agentu.md#12-zlepšování) |
| 06:32 | AI psychóza jako doložený jev — proč nestavět agenta na vztahu | [Antivzory](../01-principy/PRINCIPY-stavby-agentu.md#15-antivzory) |
| 46:43 | Model nechápe, co říká — je to prediktor dalšího slova | [Základní princip](../01-principy/PRINCIPY-stavby-agentu.md#1-základní-princip) |

---

## Knižní zdroj

**Michael Albada — _Building Applications with AI Agents: Designing and
Implementing Multiagent Systems_** (O'Reilly, září 2025, ISBN 978-1-098-17650-1).

355 stran, 13 kapitol podle životního cyklu agenta. Nejbližší strukturní
protějšek našeho build předpisu; kapitoly 9–13 (měření, monitoring, zlepšovací
smyčky, bezpečnost, spolupráce s člověkem) pokrývají fáze, které se u nás
odbývaly jednou odrážkou.

Co jsme si z ní vzali do `sablony/BUILD-PREDPIS.md`:

| Odkud | Co konkrétně |
|---|---|
| kap. 3 | textové rozhraní nemá menu — agent musí sám říct, co umí |
| kap. 4 | princip nejmenší moci u nástrojů; vypnutí nástrojů konfigurací v testu |
| kap. 9 | metriky tool recall / precision, parameter accuracy, phrase recall, task success |
| kap. 10 | rozlišení chyby od rozptylu (3–5 běhů, práh 80 %); běh naslepo vedle ostré; PSI na posun rozdělení |
| kap. 11 | rozpočet na eskalace (~10 % případů); dokumentovat každou změnu promptu |
| kap. 12 | doložený případ agenta, který „optimalizoval" produkční databázi mazáním řádků |
| kap. 13 | růst autonomie vykonavatel → kontrolor → spolupracovník → správce; čtyři způsoby selhání lidského dohledu; Klarna jako varování před opačným postupem |

Kniha stojí na LangGraphu a na týmech s ML inženýry a SRE. Pro sólo provoz
nad Cloudflare je půlka obsahu (GPU škálování, multiagentní koordinace,
fine-tuning) mimo záběr — vzali jsme principy, ne stack.

---

## Doplňkové zdroje

- **Anthropic** — *Building effective agents* a navazující materiály
  k návrhu agentických systémů (workflow vs. agent, kdy stačí prompt chain).
- **OpenAI** — *A practical guide to building agents* (nástroje, guardrails,
  eskalace na člověka).
- **AI Act** — povinnost označit, že komunikuje AI. Stav k srpnu 2026,
  po vstupu Digital Omnibus v platnost 27. 7. 2026. Termíny se mění, ověřuj.

## Pravidlo pro další zdroje

Když přibude další rozhovor, přednáška nebo studie: přepis nebo PDF
do `00-zdroje/prepisy/` (mimo git), sem řádek s citací a mapa časů.
Do metodiky v `01-principy/` patří jen závěr, ne surovina.
