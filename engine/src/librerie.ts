/** Le librerie sono DATI, non regole. Entrano nel motore nel formato esatto delle
 *  tabelle Supabase `variante` e `workout_forza`; i numerici possono arrivare come
 *  stringhe (è così che PostgREST serializza `numeric`), e qui si normalizzano. */

export type Dominio = "LOW" | "MOD" | "HIGH";

/** Riga della tabella `variante` (= una riga di lib.json / variante.csv). */
export interface VarianteRow {
  cod: string; base: string; arch: string; disc: string;
  ob_libro?: string | null; zona?: string | null; ob?: string | null;
  dist?: number | string | null; tempo: number | string;
  edw: number | string; ban?: number | string | null; rtss: number | string;
}

export interface Variante {
  cod: string; base: string; arch: string; disc: string;
  ob_libro: string; zona: string; ob: string;
  dist: number; tempo: number; edw: number; ban: number; rtss: number;
  dom: Dominio;
}

/** Riga della tabella `workout_forza` (= forza_sess2.componi, esportata da make_csv.py). */
export interface WorkoutForzaRow {
  cod: string; nome: string; bersaglio?: string | null; fasi: string;
  n_esercizi?: number | string | null; minuti: number | string;
  famiglia: string; zona: string; nm?: number | string | null;
  fatica?: number | string | null; doms: number | string;
  collocazione?: string | null;
  n_nuoto: number | string; b_bici: number | string; c_corsa: number | string;
  /** ordine canonico dei 16 workout (colonna aggiunta in Supabase); se assente
   *  vale l'ordine in cui le righe sono passate. */
  ordine?: number | string | null;
}

export interface WorkoutForza {
  cod: string; nome: string; bersaglio: string; fasi: string;
  n: number; minuti: number; famiglia: string; zona: string; nm: number;
  fatica: number; doms: number; collocazione: string;
  N: number; B: number; C: number;
}

const DOM: Record<string, Dominio> = { Z1: "LOW", Z2: "LOW", Z3: "MOD", Z4: "HIGH", Z5: "HIGH" };
const num = (x: unknown, d = 0): number => (x === null || x === undefined || x === "" ? d : Number(x));

/** Ordinamento per `cod`: rende il motore indipendente dall'ordine in cui la
 *  sorgente restituisce le righe (un risultato SQL senza ORDER BY non ne ha uno). */
export function normalizzaVarianti(rows: VarianteRow[]): Variante[] {
  const out = rows.map((r) => ({
    cod: r.cod, base: r.base, arch: r.arch, disc: r.disc,
    ob_libro: r.ob_libro ?? "", zona: r.zona ?? "", ob: r.ob ?? "",
    dist: num(r.dist), tempo: num(r.tempo), edw: num(r.edw), ban: num(r.ban), rtss: num(r.rtss),
    dom: DOM[r.zona ?? ""] ?? "LOW",
  }));
  out.sort((a, b) => (a.cod < b.cod ? -1 : a.cod > b.cod ? 1 : 0));
  return out;
}

export function normalizzaWorkout(rows: WorkoutForzaRow[]): WorkoutForza[] {
  const idx = rows.map((r, i) => ({ r, i, o: r.ordine === null || r.ordine === undefined ? i : num(r.ordine) }));
  idx.sort((a, b) => a.o - b.o || a.i - b.i);
  return idx.map(({ r }) => ({
    cod: r.cod, nome: r.nome, bersaglio: r.bersaglio ?? "", fasi: r.fasi,
    n: num(r.n_esercizi), minuti: num(r.minuti), famiglia: r.famiglia, zona: r.zona,
    nm: num(r.nm), fatica: num(r.fatica), doms: num(r.doms), collocazione: r.collocazione ?? "",
    N: num(r.n_nuoto), B: num(r.b_bici), C: num(r.c_corsa),
  }));
}
