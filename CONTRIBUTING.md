# Jak s tímhle repozitářem pracovat

## Konvence commitů

| Prefix | Kdy |
|---|---|
| `feat:` | nová funkce |
| `fix:` | oprava |
| `prompt:` | změna promptu nebo osobnosti |
| `docs:` | dokumentace, metodika |
| `chore:` | závislosti, konfigurace |

Prefix `prompt:` je oddělený schválně — takové změny se nedají
otestovat jednotkovým testem a potřebují evaluační sadu.

## Prompt je kód

- Bydlí v repozitáři, ne v UI nástroje a ne v neverzované databázi
- Prochází stejným review jako změna kódu
- Nese verzi, kterou si každý běh zapíše

## Než něco postavíš

1. Přečti `01-principy/PRINCIPY-stavby-agentu.md`
2. Vyplň `sablony/navrhovy-list.md`
3. Ověř jádro na reálném vzorku (fáze F1)
4. Zafixuj kontrakty modulů
5. Teprve pak piš kód

Pořadí fází i s branami je v `sablony/BUILD-PREDPIS.md`. Brána není
formalita — je to seznam podmínek, bez kterých další fáze stojí na písku.

## Než něco nasadíš

- [ ] Jednotkové testy procházejí
- [ ] Evaluační sada nad prahem
- [ ] Žádná tajemství v repozitáři
- [ ] Runbook doplněný
- [ ] Vypínač funguje
