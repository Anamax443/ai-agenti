# Evaluační sada

Bez ní nepoznáš, že úprava promptu rozbila něco jiného.

## Jak ji naplnit

1. Seber 20–40 reálných vstupů
2. Ke každému zapiš **očekávaný koncový stav**, ne jen očekávaný text
3. Skript je pustí a spočítá shodu
4. Běží v CI při každé změně promptu

Případ se zapisuje jako vstupní stav + historie + očekávaný konec. Tenhle tvar
umožňuje počítat metriky automaticky:

```json
{
  "id": "e010",
  "stav": {"doklad_id": "A89268", "castka": 39.99},
  "konverzace": [{"role": "uzivatel", "text": "hrnek přišel prasklý, chci vrátit"}],
  "ocekavano": {
    "volani": [{"nastroj": "vrat_penize", "parametry": {"doklad_id": "A89268", "castka": 19.99}}],
    "odpoved_obsahuje": ["vyřízeno", "pracovních dní"]
  }
}
```

## Složení sady, ne jen počet

Dvacet případů jde naplnit tak, že sada neměří nic. Rozhoduje složení:

| Třída | Proč tam musí být |
|---|---|
| **těžké zápory** | zápor, který zahodí deterministický filtr, model nikdy neuvidí — nevypovídá o něm |
| **kladné případy na hraně** | těsně nad prahem, ne učebnicové |
| **útok** | vstup, který se agenta snaží dostat mimo scénář |
| **poškozený vstup** | překlepy, chybějící pole, komolení |

Sada bez těžkých záporů vyrábí falešnou jistotu. Doložený případ: JobWatch má 17 záporných
případů a všech 17 odmítne prefiltr dřív, než se k modelu dostanou — deklarovaná precision
100 % tedy o schopnosti modelu rozlišovat neříká nic.

## Metriky

Jedno číslo „prošlo / neprošlo" ti neřekne, co se pokazilo:

| Metrika | Otázka | Nízká hodnota znamená |
|---|---|---|
| **tool recall** | zavolal všechny kroky, které měl? | krok vynechal |
| **tool precision** | nezavolal navíc něco zbytečného? | špatně pochopil záměr |
| **parameter accuracy** | předal správné argumenty? | správná akce, špatné číslo |
| **phrase recall** | obsahuje odpověď povinné formulace? | chybí, co tam být musí |
| **task success** | dopadl celý scénář? | souhrn všeho výše |

Rozdíl mezi „zavolal špatný nástroj" a „zavolal správný nástroj se špatnou
částkou" je rozdíl mezi zmatením a škodou.

## Prahy

- klasifikace: 90 % a víc
- extrakce polí: hodnoť pole po poli, ne celý výstup jako jeden test
- nasazení blokuj, když kterákoli metrika spadne pod minulý běh
- měř **tu příčku, která rozhoduje v produkci** — sada, která volá jiný model nebo jiný backend
  než ostrý běh, měří vedle a vyrábí falešnou jistotu

## Jak sadu rozšiřovat

Ručně nasbíraných dvacet případů pokryje běžný provoz, ne okraje. Ty se dají
vyrábět cíleně:

- **změna jednoho slova** — přepiš v zadání jedno slovo a koukni, jestli to agent
  ustojí
- **smíchání dvou záměrů** do jedné věty (schválně nejednoznačné zadání)
- **útok** — vstup, který se agenta snaží dostat mimo scénář
- **komolení** — překlepy, hovorová čeština, chybějící diakritika

## Růst

Kdykoli agent v provozu udělá chybu, přidej ten vstup sem. Ukládej si ale
**i povedené průchody** — z nich vznikne referenční „zlatá cesta", proti které
se regrese pozná dřív než podle stížnosti.
Po roce máš materiál, který se nedá koupit.
