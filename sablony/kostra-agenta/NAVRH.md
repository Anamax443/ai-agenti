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

---

## Vstupy

| Kanál | Kdo smí | Ověření identity |
|---|---|---|
| | | |

Identita se váže na kanál (telefonní číslo, ID, podpis webhooku),
nikdy na jméno v textu.

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

## Moduly

| ID | Modul | Kontrakt (vstup → výstup) | Závisí na |
|---|---|---|---|
| M1 | | | — |
| M2 | | | |

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
