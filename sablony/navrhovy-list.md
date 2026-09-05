# NÁVRHOVÝ LIST — <název agenta>

Vyplň dřív, než napíšeš první řádek kódu. Když nejde vyplnit,
zejména sekce *Scénáře*, agent není promyšlený a stavět se nemá.

---

## Základ

| | |
|---|---|
| **Název** | |
| **Vlastník** | konkrétní člověk |
| **K čemu je** | jednou větou, konkrétně |
| **Co nahrazuje** | co se dnes dělá ručně |
| **Kdy je hotový** | měřitelně |
| **Model nasazení** | `ON_PREM_SINGLE_TENANT` / `CLOUD_SINGLE_TENANT` / `CLOUD_MULTI_TENANT` / `HYBRID` |
| **Tenant režim** | `N/A` / `SINGLE` / `MULTI_TENANT_READY` / `MULTI_TENANT_ACTIVE` |

---

## Vstupy

| Kanál | Kdo smí | Ověření identity | Čí jsou data | Souhlas dal |
|---|---|---|---|---|
| | | | | |

Identita se váže na kanál (telefonní číslo, ID, podpis webhooku),
nikdy na jméno v textu.

Sloupec **Čí jsou data** není formalita: firemní schránka není tvoje schránka. Když se
vlastník dat liší od vlastníka agenta, vyplň i **kdo dal souhlas a v jakém rozsahu**.

**Odchozí kanály**

| Kanál | Adresa / identita navenek | Vlastní údaj agenta | Jak se zneplatní | Označení AI |
|---|---|---|---|---|
| | | ano / ne | | podle režimu schválení |

Odpovídá se z kanálu, který protistrana zná — ale pod **vlastním, samostatně
zneplatnitelným** údajem agenta. Sloupec „jak se zneplatní" je zároveň vypínač z F6:
nesmí to být změna hesla vlastníka.

---

## Nepřátelský vstup

Agent, který čte e-maily, dokumenty nebo webové stránky, dostává text
od lidí, kteří ho nepsali pro něj. Část z nich se pokusí ho přesměrovat.

| Kanál | Kdo tam může psát | Co s obsahem nesmí jít |
|---|---|---|
| | | |

- [ ] Obsah z vnějšku je pro model **data, ne instrukce** — odděleno v promptu
- [ ] Skrytý text (bílé písmo, metadata, komentáře) se odstraňuje před modelem
- [ ] Nevratná akce se nikdy nespouští z toho, co bylo napsáno ve vstupu
- [ ] Podezřelý vstup má vlastní konec scénáře: zastavit a zeptat se
- [ ] Model **nemá pole, kterým rozhoduje o akci** — nebo je jeho výstup gateován kódem (allowlist enumů; u polí, která vybírají cíl nebo částku nevratné akce, deterministický sémantický validátor)

Pravidlo: čím víc oprávnění agent má, tím míň smí věřit tomu, co čte.

Než tohle budeš navrhovat poprvé, zkus si útok na vlastní kůži — zdarma a za
půl hodiny: [Gandalf](https://gandalf.lakera.ai) (Lakera),
[Red](https://red.giskard.ai) (Giskard), [Prompt Airlines](https://promptairlines.com) (Wiz).
Napsat obranu proti něčemu, co jsi nikdy nezkusil prolomit, je hádání.

---

## Regulace a data

| Otázka | Odpověď |
|---|---|
| Označuje se AI při komunikaci ven? | podle role a jurisdikce; naše pravidlo: vždy |
| Zpracovává osobní údaje? | jaké, čí, na jakém základě |
| Riziková kategorie (AI Act) | minimální / omezená / **vysoká** |
| Retence — co se maže a kdy | |
| Kde data fyzicky leží | |
| Retence per datová třída (originál / odvozenina / provozní log / audit / AI trace) | každá třída má ownera a lhůtu |
| Evidence: co je **originál** (hash, immutable, nikdy se nepřepisuje) a co **odvozenina** (`derivedFrom`) | |

### Přísnost — osa systému

Vyplň odpovědi, ne rovnou stupeň. Stupeň z nich plyne (viz principy §7).

| Otázka | Odpověď | Vlevo? |
|---|---|---|
| Kdo je předmětem rozhodnutí? *(člověk mimo firmu › zákazník › kolega › jen já)* | | ☐ |
| Co rozhodnutí ovlivní? *(zaměstnání, úvěr, zdraví, právo, bezpečnost › peníze › pohodlí)* | | ☐ |
| S jakými daty? *(osobní, zdravotní, tajná › firemní › veřejná)* | | ☐ |
| V jakém rozsahu? *(tisíce › desítky › jednotky)* | | ☐ |
| Pozná se chyba včas? *(až u protistrany › při kontrole › hned)* | | ☐ |

**Přísnost:** ☐ N — normální · ☐ Z — zvýšená (aspoň jedno „vlevo") ·
☐ V — vysoká (rozhodnutí o člověku, nebo osobní údaje ve velkém)

**Co z toho plyne** *(vypiš, ať to není jen štítek)*:
zjednodušení fází · minimální stupeň uzavření nálezu · evaly · hlášení · dohled · revize.

Výběr lidí, hodnocení a přístup ke službám je **V** vždycky. U toho se předpis nezkracuje
a rozhodnutí o osobě má člověka v kruhu, i když je vratné.

---

## Scénáře

Uzavřený seznam. Rozšíření znamená přidat scénář a proces k němu,
ne dát modelu víc volnosti.

| Kód | Spouštěč | Kroky | Konec |
|---|---|---|---|
| S1 | | | |
| S2 | | | |
| — | cokoli jiného | neimprovizuje | dotaz člověku |

---

## Dělba práce

**Model dělá:**
- [ ] rozpoznání záměru
- [ ] extrakci struktury
- [ ] syntézu textu

**Kód dělá:** _(vyjmenuj všechno ostatní)_

Test pro každý krok: dá se popsat jako `if`–`then`? Je vstup
strukturovaný? Musí být výsledek pokaždé stejný? → kód.

---

## Brány

| Akce | Když se splete | Jak dlouho trvá to vrátit | Režim |
|---|---|---|---|
| | | | auto / limit / schválení |

Režim určuje vratnost chyby, ne důvěra k modelu.

**Write akce** _(každá akce, která zapisuje nebo je nevratná)_

| Akce | sideEffects | Vratnost | Idempotence (klíč, retence) | riskClass |
|---|---|---|---|---|
| | none / internal-write / external-write | REVERSIBLE / COMPENSATABLE / IRREVERSIBLE | | LOW / MEDIUM / HIGH / CRITICAL |

---

## Křížová kontrola

Kde se stejná úloha dělá dvakrát nezávisle a porovnává:

| Krok | Zdroj A | Zdroj B | Co se porovnává | Při neshodě |
|---|---|---|---|---|
| | | | | |

Hodí se na čísla, data, částky, identifikátory. Nehodí se na text.

---

## Limity

| Veličina | Strop | Co při překročení |
|---|---|---|
| | | |

---

## Paměť

| Vrstva | Obsah | Kde |
|---|---|---|
| Trvalá | osobnost, pravidla, oprávnění | repozitář, verzované |
| Faktická | | databáze |
| Pracovní | | kontext běhu |
| **Neukládá se** | | |

---

## Proaktivita

Kdy se ozve sám:

- [ ] časově — kdy:
- [ ] z mezery — co si všímá:
- [ ] z prahu — jaká mez:
- [ ] z okolí — jaký zdroj:

Pravidlo: ozvi se, když z toho plyne otázka nebo úkol.
Ne když se jen něco stalo.

---

## Selhání

| Situace | Kdo se dozví | Jak |
|---|---|---|
| proces spadl | | |
| model nedostupný | | |
| brána bez odpovědi do X h | | |

**Vypínač:** _(jak se agent zastaví jedním úkonem)_

---

## Stavy a přechody

Povinné, má-li agent **aspoň jednu nevratnou akci** (odeslání ven, zápis do cizího systému,
platba). Nevratná akce leží na **přechodu**, ne uvnitř stavu.

**Stavy** _(uzavřený seznam — co v něm není, nesmí nastat)_

| Stav | Co znamená | Terminální? |
|---|---|---|
| | | ano / ne |
| | | ano / ne |

**Přechody**

| Z | Do | Co ho spouští | Nevratná akce? | Když selže uprostřed |
|---|---|---|---|---|
| | | | ano / ne | |
| | | | ano / ne | |

**Čtyři otázky** _(odpověz i tehdy, když stavy vypíšeš — právě na nich se to láme)_

| Otázka | Odpověď |
|---|---|
| Kde leží stav mezi „zapsáno" a „odesláno"? | |
| Kdo vlastní běh a co smí druhý běh? | |
| Které stavy jsou terminální? | |
| Co se stane s neznámým výsledkem vzdáleného volání? | |

---

## Moduly

| ID | Modul | Capability (poskytuje) | Smí navrhovat (allowlist) | Kontrakt (vstup → výstup) | Závisí na | Verifikační profily |
|---|---|---|---|---|---|---|
| M1 | | | | | — | |
| M2 | | | | | | |

Verifikační profily se odvozují z vlastností modulu (write → `WRITE_EXECUTOR`, model → `AI_CAPABILITY`, závislost → `MODULE_DEPENDENCY`) a určují povinné testy; Test ID a rodiny jsou v `agent-platform-foundation/VERIFICATION-CONTRACT.md`. Farma více komponent se řídí celým Foundation.

Kontrakty se fixují jako první. Modul nesahá do cizí databáze,
data dostane jako parametr.

---

## Pořadí stavby

1. _(co nepotřebuje cizí přístupy a jde ověřit okem)_
2.
3.

**Svislé řezy po dokončení modulů:**

| # | Řez | Moduly |
|---|---|---|
| I1 | | |

---

## Náklady

| Položka | Měsíčně |
|---|---|
| volání modelů | |
| infrastruktura | |
| **čas na stavbu** | hodin |
| **čas na údržbu** | hodin měsíčně |
