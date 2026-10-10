# Triathlon engine

Motore di generazione del piano di allenamento. Le regole non stanno qui: stanno nel
**Manuale del piano di allenamento**, scheda *La dottrina*
(https://claude.ai/artifact/PhsWRKtkHCCRm71GUBpe6s). Questo repo contiene il codice che le
esegue e i dati che interroga.

## Struttura

| File | Che cosa fa |
| --- | --- |
| `scala_gen.py` | livello 1: quale gradino della scala e' raggiungibile. I due cancelli (ore, tempo), la distribuzione E7 |
| `generatore.py` | livello 2: genera le sedute del blocco. 8 fasi, forza periodizzata, 18 verifiche |
| `parser.py`, `dati*.py` | il libro trascritto: prosa -> 2.094 blocchi, 64 regex |
| `variazioni.py` -> `lib.json` | 9.169 varianti plausibili e non ridondanti su 18.249 generate |
| `forza_lib.py`, `forza2.py` | 184 esercizi; fatica, DOMS e collocazione DERIVATI da regole esplicite |
| `forza_sess2.py` | 16 workout standardizzati |
| `soglie.py` -> `soglie.json` | stima delle soglie dai tempi di gara (Riegel, CSS, prova oraria) |
| `scala2.py`, `forma.py` | ore dei piani del libro, indici di forma (CTL/ATL/TSB) |
| `make_csv.py` -> `csv/` | esporta le librerie nel formato delle tabelle Supabase |

`lib.json` e le librerie di forza sono **dati, non regole**, e sono rigenerabili dal codice.

## Database

Progetto Supabase `Triathlon Engine` (eu-central-1), schema derivato dal contratto dei dati
C1-C8 della dottrina. Principio: quasi nulla si aggiorna, si aggiunge.

- dati dell'atleta: `atleta`, `obiettivo`, `test`, `soglia`, `piano_versione`,
  `seduta_prescritta`, `seduta_eseguita`, `benessere`, `prontezza`, `allerta`, `decisione`
- librerie: `variante`, `esercizio`, `workout_forza`, `workout_esercizio`

Le tabelle dei dati dell'atleta hanno RLS attiva e nessuna policy: chiuse finche' non esiste
l'autenticazione.
