# <název agenta>

Kostra repozitáře pro nového agenta. Zkopíruj složku, přejmenuj,
vyplň návrhový list a začni od modulu s nejmenší závislostí.

## Struktura

| Cesta | Obsah |
|---|---|
| `NAVRH.md` | vyplněný návrhový list — první věc, kterou napíšeš |
| `prompts/` | osobnost a instrukce, verzované jako kód |
| `evals/` | regresní sada, běží v CI při každé změně promptu |
| `src/` | moduly podle kontraktů z návrhu |
| `runbook.md` | co dělat, když se to rozbije |

## Pravidla

- Prompt je kód: prochází review, nese verzi, zapisuje se do běhu.
- Modul nesahá do cizí databáze. Data dostane jako parametr.
- Každý modul má CLI a jde spustit bez zbytku systému.
- Testovací prostředí nemá odesílací kanály — konfigurací, ne přes `if`.
