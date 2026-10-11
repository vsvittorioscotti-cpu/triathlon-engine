# engine — il motore in TypeScript

Porting 1:1 di `scala_gen.py` (livello 1, la scala) e `generatore.py` (livello 2, il
generatore). Le regole non stanno qui: stanno nel Manuale, scheda *La dottrina*.
Nessuna dipendenza a runtime; il bundle `dist/engine.js` espone il globale
`TriathlonEngine` e si innesta nell'artefatto web *Ironman 226*.

| File | Che cosa fa |
| --- | --- |
| `src/scala.ts` | `livelloScala`, `fabbisognoOre`, `verificaI8` — i due cancelli, E7, le 6 verifiche |
| `src/generatore.ts` | `generaBlocco` — 8 fasi, forza periodizzata, scelta dalla libreria, le 18 verifiche |
| `src/librerie.ts` | tipi delle tabelle `variante` e `workout_forza` e la loro normalizzazione |
| `src/index.ts` | `generaPiano(input, varianti, workouts)` — scala + un blocco per gradino |
| `src/py.ts` | `pyRound` / `pyFixed`: arrotondamento "half to even" come Python, per la parità |
| `test/parita.mjs` | confronta l'output TS con i riferimenti Python in `test/ref/` |
| `test/genera_ref.py` | rigenera i riferimenti dal Python (da lanciare dalla radice del repo) |

## Uso

```
cd engine
npm install          # solo esbuild e typescript, per compilare
npm run build        # dist/engine.js (IIFE, globale TriathlonEngine) e dist/engine.mjs
npm test             # build + test di parità
```

```ts
import { generaPiano } from "./dist/engine.mjs";
const piano = generaPiano(
  { gradino_fatto: null, settimane: 26, ore_disponibili: 11, ore_oggi: 5, obiettivo: "Ironman" },
  righeVariante,      // select * from variante
  righeWorkoutForza,  // select * from workout_forza order by ordine
);
```

Le librerie entrano nel formato esatto delle tabelle Supabase: i numerici possono arrivare
come stringhe. Il motore ordina le varianti per `cod` e i workout per `ordine`, così il
risultato non dipende dall'ordine in cui la sorgente restituisce le righe.

## Parità con il Python

`npm test` confronta 10 casi della scala e 8 blocchi generati (settimane, sedute, numeri a
1e-9, e le verifiche con i loro testi). I riferimenti committati sono un sottoinsieme;
`python3 engine/test/genera_ref.py` li rigenera tutti (serve `openpyxl` per importare
`generatore.py`, anche se poi legge `lib.json`).

Una sola modifica al Python è stata necessaria: `generatore.py` ordina `LIB` per `cod`,
perché in un caso (`im36_11`) una seduta cambiava a seconda dell'ordine del file.
