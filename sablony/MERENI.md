# MĚŘENÍ — jak se agent měří proti etalonu

> 🇨🇿 Čeština · [🇬🇧 English](MERENI.en.md)

Audit napsaný volným textem je čtivý a **neporovnatelný**. Dva měřiči napíšou dva různé
dokumenty a nejde z nich odečíst, jestli se shodli. Etalon, u kterého to nejde, není etalon —
je to názor s tabulkami.

Tenhle list je proto formulář, ne esej.

## Prázdný formulář se generuje, neopisuje

```bash
python kontrola/brany.py --protokol v0.10 > 02-pripady/MERENI-<agent>.md
```

Formulář se odvozuje přímo z [`BUILD-PREDPIS.md`](BUILD-PREDPIS.md). **Druhý seznam podmínek
neexistuje** a existovat nemá: dokud se počet psal ručně, rozešel se — v jednom dokumentu
stálo postupně 38, 37, 41 a 42 na čtyřech místech a našla to až cizí recenze.

Vyplněné měření je **záznam**, ne dokument metodiky — buď mu dopiš anglické dvojče, nebo
ho zapiš do [`kontrola/bez-prekladu.txt`](../kontrola/bez-prekladu.txt), ať kontrola dvojic
projde a chybějící překlad je přitom vidět.

Inventář a kontrolu si vypíšeš takhle:

```bash
python kontrola/brany.py            # kontrola: shoda počtu podmínek CS × EN
python kontrola/brany.py --seznam   # inventář s identifikátory
```

## Co se u každé podmínky vyplňuje

| Pole | Hodnoty | Kdy je povinné |
|---|---|---|
| **Výsledek** | `ano` · `ne` · `nelze` · `neměřeno` | vždy |
| **Stupeň** | `U0`–`U4` | u `ano` **i u `ne`** |
| **Důkaz / poznámka** | soubor, test, příkaz **s výstupem** | u `ano`, `ne` a `nelze`; u `neměřeno` napiš, co by bylo potřeba |

### Čtyři výsledky, ne dva a půl

| Výsledek | Znamená |
|---|---|
| `ano` | splňuje, a je to doložené na uvedeném stupni |
| `ne` | **nesplňuje** — a stupeň říká, jak dobře to víš |
| `nelze` | brána na tohohle agenta **nesedí** (např. eskalace u agenta, který žádné nemá) |
| `neměřeno` | dala by se změřit, ale **měřič to neudělal** |

`nelze` a `neměřeno` nejsou totéž a slévat je do `ne` je chyba: `ne` tvrdí, že agent podmínku
porušuje. Doplněno 2. 9. 2026 po prvním vyplněném protokolu, kde tři položky tuhle hodnotu
potřebovaly a nebyla.

**Podíl `neměřeno` je metrika poctivosti měření**, ne ostuda měřiče. Protokol se samými
`ano`/`ne` je podezřelý — 49 podmínek nikdo neověří všechny.

### Stupně uzavřenosti

| | Význam | Kdo o tom ví |
|---|---|---|
| **U0** | tvrzeno — autor říká, že to platí | autor |
| **U1** | v kódu — změna je v repozitáři a dá se přečíst | kdokoli, kdo čte |
| **U2** | kryto testem — test selže, když se to rozbije | CI |
| **U3** | vyvoláno v prostředí — stav skutečně nastal | provoz |
| **U4** | nezávisle uzavřeno — ověřil někdo jiný než autor opravy | třetí strana |

Minimální stupeň, na kterém se smí podmínka uzavřít jako `ano`, **určuje přísnost agenta**
(N → U1, Z → U2, V → U3; viz [principy §7](../01-principy/PRINCIPY-stavby-agentu.md)).

**Stupeň se vyplňuje i u `ne`.** „Nesplňuje, protože jsem to vyvolal" a „nesplňuje, protože
jsem si přečetl kód" nejsou totéž. Stupnice se ptá pořád na jedno — **čím to víš** — a ta otázka
platí pro obě odpovědi. U `ne` se minimální stupeň nevymáhá; slouží k tomu, aby šlo poznat, jak
pevný ten nález je.

**Původ přísnosti se zapisuje.** Když ji neurčuje návrhový list, ale až měřič, je to zároveň
výsledek `ne` u podmínky F0.4 — etalon by jinak žádal vstup, který sám vyrábí.

### Dvě pravidla, bez kterých je formulář k ničemu

**`nelze` je plnohodnotný výsledek.** Bez něj se měřič tlačí do `ano`/`ne` i tam, kde brána
na daného agenta nesedí. Přesně tak vznikl spor o bránu F4 u agenta, jehož výchozí backend
existuje jen za běhu: v CI by se měřil jiný model než ten, který rozhoduje. Brána tehdy
nutila buď lhát, nebo měřit vedle — a měla dostat `nelze` s poznámkou, ne `ne`.

**U `ano` je povinný důkaz, a příkaz sám důkaz není.** Důkazem je jeho **výstup**, uložený
artefakt nebo test. Bez toho platí nejvýš `U0`, i kdyby to byla pravda.

## Souhrn a kalibrace etalonu

Na konci formuláře jsou dva bloky. První je počet `ano` / `ne` / `nelze`. Druhý je
důležitější a snadno se vynechá:

> **Nálezy, které měření nenašlo.**

Doplňuje se **později**, když se vada objeví jinudy — z provozu, z cizí recenze, z incidentu.
Není to ostuda měřiče, je to **jediné číslo o přesnosti samotného etalonu**.

Dnes je doložené jedno: při prvním ostrém použití našel předpis **4 z 8** vad, které se
u téhož agenta nakonec prokázaly. Chytil vypínač, tiché selhání, cizí text bez obalu
a neměřitelný prompt; **neodhalil ani jednu ze čtyř vad v orchestraci.** Záchytnost 50 %
na jednom vzorku je slabé číslo — ale etalon, který svoje číslo nemá, je horší.

> Že by dnešní znění chytilo 8 z 8, **není měření**. Ty položky vznikly z těch vad, takže
> by to bylo zpětné doladění. Proto se měří vždy proti **vydání** etalonu, ne proti
> aktuálnímu `main`.

## Vydání etalonu

Měření se odkazuje na vydání, ne na větev:

```
Etalon: ai-agenti v0.10  (git tag v0.10)
```

Poziční identifikátory (`F3.4`) platí **uvnitř vydání**. Po vložení nové podmínky se posunou,
a to je v pořádku — jejich význam pevně určuje verze. Normy to dělají stejně:
`ISO 27001:2013 A.9.2.3` znamená něco jiného než tentýž kód ve vydání 2022.

**Během měření se etalon nemění.** Změny, které z měření vzejdou, patří do dalšího vydání
a ověřují se až na dalším případu — jinak si etalon dolaďuje sám sebe na to, co právě viděl.

## Opakovatelnost

Etalon, který umí použít jen jeho autor, není etalon. Ověřuje se to jediným způsobem:
**dva měřiči, tentýž agent, tentýž formulář — a rozdíl mezi formuláři se odečte.**

Zatím to nikdo neudělal. Do té doby je opakovatelnost neznámá, a měření podepsané autorem
předmětu se počítá jako sebehodnocení, ne jako nezávislé měření.
