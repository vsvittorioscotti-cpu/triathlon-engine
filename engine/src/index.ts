/** Triathlon engine — punto d'ingresso.
 *  Livello 1: livelloScala / fabbisognoOre / verificaI8 (scala.ts)
 *  Livello 2: generaBlocco (generatore.ts)
 *  Orchestrazione: generaPiano = scala + un blocco per gradino. */
export * from "./scala";
export * from "./generatore";
export * from "./librerie";
export { pyRound, pyFixed } from "./py";

import { livelloScala, fabbisognoOre, verificaI8, isErrore, RITENZIONE } from "./scala";
import type { Gradino, PianoScala, ErroreScala, Fabbisogno, Verifica } from "./scala";
import { generaBlocco } from "./generatore";
import type { PianoBlocco } from "./generatore";
import { normalizzaVarianti, normalizzaWorkout } from "./librerie";
import type { VarianteRow, WorkoutForzaRow } from "./librerie";

export interface InputAtleta {
  gradino_fatto?: string | null;   // ultimo gradino completato, null/undefined = da zero
  settimane: number;               // settimane alla prima gara utile
  ore_disponibili: number;         // ore/settimana dichiarate (tetto o fabbisogno)
  ore_oggi: number;                // ore/settimana attuali
  obiettivo?: Gradino;             // default Ironman
  tetto_rigido?: boolean;          // default false
  sedute_sett?: number;            // default 8
  giorno_riposo?: string;          // default "Lunedì"
}

export interface PianoCompleto {
  scala: PianoScala;
  fabbisogno: Fabbisogno[];
  verifiche_scala: Verifica[];
  blocchi: PianoBlocco[];          // uno per gradino, nell'ordine della scala
}

/** Scala + generazione di ogni blocco. Le librerie arrivano nel formato delle
 *  tabelle Supabase (righe grezze); qui vengono normalizzate una volta. */
export function generaPiano(input: InputAtleta, varianti: VarianteRow[], workouts: WorkoutForzaRow[]): PianoCompleto | ErroreScala {
  const obiettivo = input.obiettivo ?? "Ironman";
  const scala = livelloScala(input.gradino_fatto, input.settimane, input.ore_disponibili,
    input.ore_oggi, obiettivo, input.tetto_rigido ?? false);
  if (isErrore(scala)) return scala;
  const lib = normalizzaVarianti(varianti);
  const wk = normalizzaWorkout(workouts);
  const blocchi: PianoBlocco[] = [];
  let inizio = input.ore_oggi;
  for (const b of scala.blocchi) {
    blocchi.push(generaBlocco({
      gara: b.gradino, settimane: b.settimane, ore_picco: b.picco, ore_oggi: inizio,
      sedute_sett: input.sedute_sett ?? 8, giorno_riposo: input.giorno_riposo ?? "Lunedì",
    }, lib, wk));
    inizio = b.picco * RITENZIONE;
  }
  return { scala, fabbisogno: fabbisognoOre(scala), verifiche_scala: verificaI8(scala, input.gradino_fatto, obiettivo), blocchi };
}
