# SCÉNÁŘ — Agent pro obsah Gwalarn

Facebook · Instagram · gwalarn.cz
Verze 1.0 · srpen 2026

---

## Východiska

- Publikuje se **jen na vlastní účty kapely** → app review u Mety není potřeba,
  stačí Meta app v development módu a role Instagram Tester.
- Web gwalarn.cz je **primární cíl**. FB a IG posty jsou jeho zkrácené deriváty
  s odkazem zpět. Jeden zdroj pravdy, tři výstupy.
- **Schválení člověkem je povinné.** Nic se nepublikuje automaticky.
- Učení stojí primárně na **dvojicích draft/final**, ne na dosahu.
  Při čtyřech příspěvcích měsíčně je vzorek pro statistiku příliš malý.

Runtime: Cloudflare Workers + D1 + R2, Telegram pro schvalování.
Navazuje na existující stack, nestaví se od nuly.

---

## Fáze 0 — Účty a přístupy

Nudná, ale blokuje všechno ostatní. Počítej s tím, že se to protáhne
na víc než jedno sezení, protože část kroků potvrzuje někdo jiný.

### Kroky

1. Instagram Gwalarn převést na **Business** účet
   (ne Creator — Creator neumí přes API publikovat Reels)
2. Propojit s Facebook stránkou kapely
3. Založit Meta app typu Business na developers.facebook.com
4. Přidat produkt Instagram Graph API
5. V dev módu přidat IG účet jako **Instagram Tester**, pozvánku přijmout
   v nastavení Instagramu
6. Vygenerovat long-lived token, poznamenat datum expirace
7. Ověřit ručně přes Graph API Explorer: vytvořit container a publikovat
   testovací obrázek

### Hotovo, když

- [ ] Testovací fotka se objevila na IG přes API, ne z telefonu
- [ ] Token uložený v Workers Secrets, ne v repozitáři
- [ ] Napsaná poznámka, kdy token vyprší

### Pasti

- Token platí 60 dní a **sám se neobnovuje**. Refresh cron je součást
  fáze 3, ale kalendářovou připomínku si dej hned.
- Personal účty přes API nefungují vůbec. Pokud má někdo z kapely dojem,
  že „to jde i bez toho", nejde.

---

## Fáze 1 — Podklady a datový model

Agent bez zdrojů píše vatu. Tahle fáze je o tom, čím ho krmit.

### Obsah k připravení

| Zdroj | Kde | Poznámka |
|---|---|---|
| Kalendář koncertů | D1 tabulka `events` | datum, místo, čas, sestava, odkaz na vstupenky |
| Fotky | R2 + tabulka `media` | **každá s popiskem** — bez toho je fotobanka k ničemu |
| Zvukové ukázky | R2 | musí projít převodem na video, viz fáze 4 |
| Identita kapely | soubor `identity.md` | píše se jednou, mění zřídka |
| Archiv publikovaného | D1 tabulka `posts` | aby se posty neopakovaly |

### Identita kapely — co do ní patří

Ne „bretonská kapela". Konkrétnosti, ze kterých má model z čeho brát:

- nástroje: biniou, bombarda, co kdo hraje
- tance a formy: an dro, hanter dro, gavotte, plinn
- kontext fest-noz — co to je a jak o tom mluvíte
- jazyk: jak píšete o bretonštině, jestli uvádíte překlady
- čemu se vyhýbat: obecná adjektiva o „magické keltské atmosféře",
  klišé o mystice, zaměňování bretonského a irského

Tenhle soubor je nejdůležitější věc v celém projektu. Rozdíl mezi vaším
postem a postem libovolné jiné folkové kapely vzniká právě tady.

### Schéma D1

```sql
CREATE TABLE events (
  id TEXT PRIMARY KEY,
  starts_at INTEGER NOT NULL,
  venue TEXT NOT NULL,
  city TEXT,
  lineup TEXT,
  ticket_url TEXT,
  note TEXT              -- cokoli specifického k téhle akci
);

CREATE TABLE media (
  id TEXT PRIMARY KEY,
  r2_key TEXT NOT NULL,
  kind TEXT NOT NULL,    -- photo | audio
  caption TEXT NOT NULL, -- povinné, jinak je fotka nepoužitelná
  event_id TEXT,
  taken_at INTEGER,
  used_count INTEGER DEFAULT 0
);

CREATE TABLE recipes (
  id TEXT NOT NULL,
  version INTEGER NOT NULL,
  body TEXT NOT NULL,
  note TEXT,
  created_at INTEGER NOT NULL,
  PRIMARY KEY (id, version)
);

CREATE TABLE posts (
  id TEXT PRIMARY KEY,
  recipe_id TEXT,
  recipe_version INTEGER,
  event_id TEXT,
  media_ids TEXT,              -- JSON pole
  platform TEXT,               -- web | facebook | instagram
  draft_text TEXT,             -- co vygeneroval model
  final_text TEXT,             -- co jsi skutečně publikoval
  edit_distance REAL,          -- míra zásahu, 0 = beze změny
  my_rating INTEGER,           -- 1-5, tvoje spokojenost
  published_at INTEGER,
  metrics_json TEXT,
  metrics_fetched_at INTEGER
);
```

### Hotovo, když

- [ ] Aspoň 20 fotek v R2, každá s popiskem
- [ ] Kalendář koncertů na půl roku dopředu
- [ ] `identity.md` přečtený a odsouhlasený zbytkem kapely

---

## Fáze 2 — Skládané prompty

Prompt se nepíše jako jedna věta. Skládá se ze tří vrstev teprve
při generování.

```
┌─ identita kapely ──────────┐  statická, mění se zřídka
├─ recept na typ příspěvku ──┤  v D1, verzovaný
├─ fakta o události ─────────┤  z events + media
└────────────────────────────┘
              ↓
        návrh příspěvku
```

### Recepty k založení

| ID | Kdy se použije | Cíl |
|---|---|---|
| `pozvanka` | 10 dní před koncertem | dostat lidi na akci |
| `pripominka` | 2 dny před koncertem | krátká, jen fakta |
| `ohlednuti` | den po koncertě | fotka, poděkování |
| `skladba` | kdykoli, výplň kalendáře | představit kus repertoáru |
| `fotka` | kdykoli | ze zkoušky, z cest |

### Jak vypadá dobrý recept

Ne „napiš pozvánku s nádechem Bretaně". Konkrétní instrukce ke struktuře:

> Dvě až tři věty. První je konkrétní pozvání s datem, místem a časem.
> Druhá odkazuje na jeden konkrétní tanec nebo skladbu z programu — vyber
> podle poznámky k akci. Žádná obecná adjektiva o atmosféře. Zakončit
> odkazem. Bez emoji na začátku vět, maximálně jedno na konci.

Recepty se ukládají do D1, ne do kódu — upravuješ je bez deploye.

### Varianty podle platformy

Ze stejných podkladů vzniknou tři výstupy různé délky:

- **web** — nejdelší, kontext, může být článek
- **facebook** — střední, snese odkaz i delší text
- **instagram** — nejkratší, těžiště na obrázku, odkaz nefunguje v popisku

### Hotovo, když

- [ ] Pět receptů v D1
- [ ] Generování běží lokálně, výstup dává smysl
- [ ] Ze stejné události vzniknou tři různě dlouhé varianty

---

## Fáze 3 — Publikační pipeline

### Tok

```
cron ──> najdi událost v okně ──> vyber recept ──> vyber fotku
   ──> vygeneruj návrh ──> ulož jako draft ──> Telegram ke schválení
   ──> [ty: schválit / upravit / zahodit] ──> publikuj ──> ulož final_text
```

### Telegram schvalování

Zpráva obsahuje: náhled textu, náhled fotky, název receptu.
Tlačítka: **Publikovat** · **Upravit** · **Zahodit**.

Úprava přijde jako odpověď textem. Uloží se do `final_text`,
`edit_distance` se dopočítá. Tohle je hlavní učicí signál — neošidit.

Po publikaci druhá zpráva: hodnocení 1–5, jak jsi spokojený.
Pět sekund práce, cennější než většina metrik.

### Publikace na Instagram

Dvoukrokové volání: nejdřív POST na `/{ig-user-id}/media` vytvoří container,
pak `/{ig-user-id}/media_publish` publikuje. Mezi tím se čeká na zpracování —
u videa i desítky sekund, je potřeba pollovat stav containeru.

### Refresh tokenu

Samostatný cron, jednou týdně. Obnoví long-lived token a pošle
do Telegramu potvrzení. Když selže, pošle varování — ne ticho.

### Hotovo, když

- [ ] Pozvánka na skutečný koncert projde celým tokem
- [ ] Úprava přes Telegram se uloží do `final_text`
- [ ] Selhání publikace skončí hláškou v Telegramu, ne tichem

---

## Fáze 4 — Zvukové ukázky

Ani Facebook, ani Instagram nepřijmou samotné audio. Musí z toho být video.

```bash
# statická fotka + zvuk
ffmpeg -loop 1 -i foto.jpg -i ukazka.mp3 \
  -c:v libx264 -tune stillimage -c:a aac -b:a 192k \
  -pix_fmt yuv420p -shortest -vf "scale=1080:1080" out.mp4

# s vykreslenou vlnou
ffmpeg -i ukazka.mp3 -filter_complex \
  "[0:a]showwaves=s=1080x300:mode=cline:colors=white[w]; \
   [1:v][w]overlay=0:390[v]" -i foto.jpg -map "[v]" -map 0:a \
  -c:v libx264 -c:a aac -shortest out.mp4
```

Kde to poběží: ffmpeg v Workers není. Buď jako job na Beelinku, který
si pro úkoly chodí sám, nebo předgenerovat videa dopředu a do R2 ukládat
už hotová.

### Hotovo, když

- [ ] Ukázka se objeví na IG jako video s obalem
- [ ] Formát 1:1 nebo 4:5, ne 16:9 — na mobilu se jinak ztratí

---

## Fáze 5 — Metriky a učení

### Sběr metrik

Samostatný cron, ne součást publikace. Po **48 hodinách** a po **7 dnech**
dojde pro insights a doplní `metrics_json`.

Pozor: u Facebook Insights se letos rušila část endpointů. Než na tom
postavíš schéma, ověř, co je ještě dostupné — a počítej s tím,
že se to změní znovu.

### Čtvrtletní revize

**Neautomatická.** Jednou za čtvrtletí spustíš úlohu, která:

1. vezme všechny posty daného receptu
2. sestaví dvojice `draft_text` / `final_text`
3. přidá metriky a tvoje hodnocení
4. nechá model napsat **návrh nové verze receptu s odůvodněním**

Ty ho přečteš a schválíš nebo zahodíš. Nová verze se uloží
jako `version + 1`, stará zůstane.

### Proč ne automaticky

Při čtyřech příspěvcích měsíčně máš po roce padesát vzorků rozdělených
mezi pět receptů a tři platformy. Rozdíl mezi „úspěšným" a „neúspěšným"
postem je v takovém vzorku většinou to, jestli jste hráli známý festival
a někdo to nasdílel. Smyčka, která si podle toho sama přepisuje prompty,
se rozjede špatným směrem a všimneš si až za rok.

### Hotovo, když

- [ ] Metriky se doplňují samy
- [ ] První čtvrtletní revize proběhla a vznikla verze 2 aspoň jednoho receptu
- [ ] Staré verze receptů jsou dohledatelné

---

## Pořadí a odhad

| Fáze | Práce | Blokuje |
|---|---|---|
| 0 · Účty | 2–3 h rozprostřené | vše |
| 1 · Podklady | 4 h + focení a psaní popisků | 2, 3 |
| 2 · Prompty | 4 h | 3 |
| 3 · Pipeline | 8 h | 4, 5 |
| 4 · Audio | 3 h | — |
| 5 · Učení | 4 h | — |

Fáze 4 a 5 jdou odložit. Fáze 0 a 1 nejdou přeskočit ani zkrátit —
a fáze 1 je jediná, kde je práce, kterou za tebe neudělá kód.

---

## Co se pokazí

- **Popisky u fotek nikdo nedopíše.** Nejčastější důvod, proč tenhle typ
  projektu skončí u nedodělané fotobanky. Udělej to dřív než pipeline.
- **Token vyprší v nejhorší chvíli.** Refresh cron a hlídání do Telegramu.
- **Meta změní API.** Stane se to, ne jestli, ale kdy. Publikační vrstvu
  drž oddělenou od zbytku, aby se dala vyměnit.
- **Agent začne psát vatu.** Signál je rostoucí `edit_distance`.
  Když roste, problém není v modelu, ale v `identity.md` nebo v receptu.
