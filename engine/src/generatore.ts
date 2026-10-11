/** Livello 2 — il generatore: dalla dottrina al piano, pescando dalla libreria.
 *  Porting 1:1 di generatore.py. Le regole sono nel Manuale (scheda "La dottrina");
 *  qui ogni costante porta, dove c'è, l'ID della regola che la giustifica. */
import { cmpTuple, pyFixed } from "./py";
import type { Dominio, Variante, WorkoutForza } from "./librerie";
import type { Gradino } from "./scala";
import type { Verifica } from "./scala";

export type Giorno = "Lunedì" | "Martedì" | "Mercoledì" | "Giovedì" | "Venerdì" | "Sabato" | "Domenica";
export type Disciplina = "Nuoto" | "Ciclismo" | "Corsa a piedi" | "Forza";
export type Fase = "Preparation" | "Base 1" | "Base 2" | "Build 1" | "Build 2" | "Specific" | "Peak" | "Taper";
export type Macro = "Preparatorio" | "Specifico" | "Taper";
export type TipoSett = "Carico" | "Scarico" | "Taper";

export interface ConfigBlocco {
  gara: Gradino;
  settimane: number;
  ore_picco: number;
  ore_oggi: number;
  sedute_sett?: number;   // accettato per contratto, non ancora usato (come in Python)
  giorno_riposo?: string; // idem
}

export interface Settimana {
  w: number; blocco: number; pos: number; macro: Macro; tipo: TipoSett; fase: Fase;
  ore: number; forza_min: number; sforamento: number;
}

export interface Seduta {
  w: number; macro: Macro; blocco: number; tipo: TipoSett;
  giorno: Giorno; disc: Disciplina; ob: string; cod: string; struttura: string;
  tempo: number; edw: number; rtss: number; dom: Dominio;
  costo?: "S1" | "S2" | "S3"; doms?: number;
}

export interface Riepilogo {
  sedute: number; ore: number; edw: number;
  ore_endurance: number; ore_forza: number;
  low: number; mod: number; high: number;      // percentuali sul tempo
  ore_max_settimana: number; distinti: number;
  mancati: Array<[string, string]>;
}

export interface PianoBlocco {
  PIANO: Seduta[]; W: Settimana[]; A: ConfigBlocco; NB: number; TAPER_DA: number;
  N_TAPER: number; riepilogo: Riepilogo; verifiche: Verifica[];
}

// ---------- 1. architettura ----------
// Otto fasi, non due macrocicli: quota di forza e sforamento cambiano per fase.
// Le frazioni sono nostre e sommano a 1 sulle settimane che precedono il taper.
const FASI: Array<[Fase, number]> = [["Preparation", 0.10], ["Base 1", 0.15], ["Base 2", 0.15], ["Build 1", 0.15],
  ["Build 2", 0.15], ["Specific", 0.18], ["Peak", 0.12]];
// quota di forza sul monte ore, e sforamento ammesso (Strength Allowance)
const QUOTA: Record<Fase, number> = { "Preparation": 0.175, "Base 1": 0.165, "Base 2": 0.135, "Build 1": 0.105,
  "Build 2": 0.085, "Specific": 0.065, "Peak": 0.040, "Taper": 0.015 };
const ALLOW: Record<Fase, number> = { "Preparation": 0.125, "Base 1": 0.090, "Base 2": 0.065, "Build 1": 0.025,
  "Build 2": 0.015, "Specific": 0.0, "Peak": 0.0, "Taper": 0.0 };
// sedute per fase: la frequenza resta a due più a lungo di quanto faccia il libro
const NSED: Record<Fase, number> = { "Preparation": 2, "Base 1": 2, "Base 2": 2, "Build 1": 2,
  "Build 2": 2, "Specific": 2, "Peak": 1, "Taper": 1 };
// carattere del contenuto per fase: quale tag della libreria e quale famiglia preferire
const CARATT: Record<Fase, [string, string | null]> = { "Preparation": ["B", null], "Base 1": ["B", "Forza massima"],
  "Base 2": ["B", "Forza massima"], "Build 1": ["U", null], "Build 2": ["U", null],
  "Specific": ["S", null], "Peak": ["P", null], "Taper": ["P", null] };

/** Blocchi di 4 (3 carico + 1 scarico). La seconda metà resta "specifica"
 *  per il piazzamento dei brick (I6); le otto fasi vivono sopra a questa. */
function architettura(n: number): [Array<[Macro, number[]]>, number] {
  const blocchi = Math.ceil(n / 4);
  const meta = Math.max(1, Math.floor(blocchi / 2));
  const range = (a: number, b: number) => Array.from({ length: Math.max(0, b - a) }, (_, i) => a + i);
  return [[["Preparatorio", range(1, meta + 1)], ["Specifico", range(meta + 1, blocchi + 1)]], blocchi];
}

// ---------- 3. scheletro settimanale ----------
// Qualità concentrata a inizio settimana, vigilia del lungo protetta.
const SKEL: Array<[Giorno, Disciplina]> = [["Martedì", "Nuoto"], ["Martedì", "Corsa a piedi"], ["Martedì", "Forza"],
  ["Mercoledì", "Ciclismo"], ["Mercoledì", "Forza"],
  ["Giovedì", "Nuoto"], ["Giovedì", "Corsa a piedi"],
  ["Venerdì", "Nuoto"],
  ["Sabato", "Ciclismo"],
  ["Domenica", "Corsa a piedi"],
  ["Lunedì", "Forza"]]; // terzo slot: solo structural, solo nelle fasi iniziali

const PESO_Z: Record<string, number> = { Z1: 1, Z2: 2, Z3: 3, Z4: 4, Z5: 5 };
const ORDINE: Record<string, number> = { S1: 1, S2: 2, S3: 3 };

/** costo della seduta secondo la classificazione S1/S2/S3 */
export function costo(d: WorkoutForza): "S1" | "S2" | "S3" {
  return d.doms >= 4 ? "S3" : d.doms === 3 ? "S2" : "S1";
}

/** S3 solo lontano dal lungo e non in vigilia di una corsa chiave.
 *  Il giovedì è a ritmo gara nelle settimane in posizione 3. */
function tettoCosto(giorno: Giorno, tipo: TipoSett, pos: number): "S1" | "S2" | "S3" {
  if (giorno === "Lunedì") return "S1";                       // terzo slot: solo lavoro economico
  if (tipo === "Taper" || tipo === "Scarico") return "S1";    // scarico e taper: solo basso costo
  if (giorno === "Mercoledì" && pos === 3) return "S2";       // giovedì qualità
  return "S3";
}

// quota di ore per disciplina (baseline Ironman misurato: bici 51 / corsa 31 / nuoto 18)
const MIX: Record<string, number> = { "Ciclismo": 0.51, "Corsa a piedi": 0.31, "Nuoto": 0.18 };
const PESO_SLOT: Record<string, number> = {
  "Sabato|Ciclismo": 0.75, "Mercoledì|Ciclismo": 0.25,
  "Domenica|Corsa a piedi": 0.40, "Martedì|Corsa a piedi": 0.30, "Giovedì|Corsa a piedi": 0.30,
  "Martedì|Nuoto": 0.38, "Giovedì|Nuoto": 0.38, "Venerdì|Nuoto": 0.24,
};

/** politica degli stimoli. Vincolo dominante: la prevalenza aerobica (I4).
 *  Al massimo UNA seduta di qualità in preparatorio, DUE nello specifico. */
export function stimolo(macro: Macro, tipo: TipoSett, giorno: Giorno, disc: Disciplina, pos = 1): string {
  if (tipo === "Taper") {
    if (giorno === "Martedì") return "Ritmo gara specifico";
    if (giorno === "Mercoledì" && disc === "Ciclismo") return "Ritmo gara specifico";
    return "Aerobico base";
  }
  if (giorno === "Venerdì") return "Recupero attivo"; // vigilia del lungo
  if (tipo === "Scarico") return giorno === "Martedì" && disc === "Corsa a piedi" ? "Soglia anaerobica" : "Aerobico base";
  if (macro === "Preparatorio") {
    if (giorno === "Martedì" && disc === "Corsa a piedi") return pos === 2 || pos === 3 ? "Soglia anaerobica" : "Aerobico base";
    if (giorno === "Domenica" && disc === "Corsa a piedi") return "Aerobico lento (lungo)";
    if (giorno === "Sabato") return "Aerobico lento (lungo)";
    return "Aerobico base";
  }
  // macrociclo specifico
  if (giorno === "Martedì" && disc === "Corsa a piedi") return pos === 2 ? "VO2max" : "Soglia anaerobica";
  if (giorno === "Mercoledì" && disc === "Ciclismo") return "Ritmo gara specifico";
  if (giorno === "Sabato" && disc === "Ciclismo") return pos === 3 ? "Ritmo gara specifico" : "Aerobico lento (lungo)";
  if (giorno === "Giovedì" && disc === "Corsa a piedi") return pos === 3 ? "Ritmo gara specifico" : "Aerobico base";
  if (giorno === "Domenica" && disc === "Corsa a piedi") return "Aerobico lento (lungo)"; // mai qualità il giorno dopo il lungo
  return "Aerobico base";
}

// vincolo di specificità: il lungo in bici deve raggiungere un pavimento nelle ultime fasi
const FLOOR_LUNGO: Record<Gradino, number> = { "Ironman": 210, "Half-Ironman": 150, "Triathlon Olimpico": 90, "Triathlon Sprint": 60 };

// vocabolario della libreria: solo questi cinque obiettivi esistono davvero
const VOC: Record<string, Dominio> = { "Recupero attivo": "LOW", "Aerobico base": "LOW", "Ritmo gara specifico": "MOD",
  "Soglia anaerobica": "HIGH", "VO2max": "HIGH" };
const TRAD: Record<string, string> = { "Aerobico lento (lungo)": "Aerobico base", "Forza specifica": "Aerobico base",
  "Capacita' anaerobica": "VO2max", "Velocita' neuromuscolare": "VO2max" };

const sum = (xs: number[]) => xs.reduce((a, b) => a + b, 0);

/** Genera le sedute di UN blocco della scala. `lib` e `workouts` già normalizzati
 *  (vedi librerie.ts). */
export function generaBlocco(A: ConfigBlocco, lib: Variante[], workouts: WorkoutForza[]): PianoBlocco {
  const WK = new Map<string, WorkoutForza>();
  for (const w of workouts) WK.set(w.cod, w);
  const MANCATI: Array<[string, string]> = [];

  // D8: durata e profondità del taper, misurate sui quattro piani del libro
  // (Sprint 1 sett. al 32% del picco; Ironman 2 sett., l'ultima al 7%)
  const N_TAPER = A.settimane <= 8 ? 1 : 2;
  const PROF_TAPER = N_TAPER === 1 ? [0.32] : [0.50, 0.10];
  const [MACRO, NB] = architettura(A.settimane);
  const TAPER_DA = A.settimane - N_TAPER + 1;

  // ---------- 2. calendario e carico settimanale ----------
  const faseDi = (w: number): Fase => {
    if (w >= TAPER_DA) return "Taper";
    const n = TAPER_DA - 1; let cum = 0.0;
    for (const [nome, q] of FASI) {
      cum += q;
      if (w <= Math.ceil(cum * n)) return nome;
    }
    return FASI[FASI.length - 1][0];
  };

  const W: Settimana[] = [];
  for (let w = 1; w <= A.settimane; w++) {
    const blocco = Math.floor((w - 1) / 4) + 1; const pos = ((w - 1) % 4) + 1;
    let macro: Macro = MACRO.find(([, bs]) => bs.includes(blocco))?.[0] ?? "Taper";
    let tipo: TipoSett;
    if (w >= TAPER_DA) { tipo = "Taper"; macro = "Taper"; }
    else if (pos === 4) tipo = "Scarico";
    else tipo = "Carico";
    W.push({ w, blocco, pos, macro, tipo, fase: faseDi(w), ore: 0, forza_min: 0, sforamento: 0 });
  }

  // rampa: ore = da ore_oggi al picco; sotto-picco 85% a fine preparatorio
  const caricoW = W.filter((x) => x.tipo === "Carico");
  const nCar = caricoW.length;
  caricoW.forEach((x, i) => {
    const frac = nCar > 1 ? i / (nCar - 1) : 0;
    x.ore = A.ore_oggi + (A.ore_picco - A.ore_oggi) * frac;
    if (x.macro === "Preparatorio") x.ore = Math.min(x.ore, A.ore_picco * 0.85);
  });
  for (const x of W) {
    if (x.tipo === "Scarico") {
      const prec = W.filter((y) => y.w < x.w && y.tipo === "Carico");
      x.ore = prec.length ? prec[prec.length - 1].ore * 0.60 : A.ore_oggi * 0.6;
    } else if (x.tipo === "Taper") {
      const k = x.w - TAPER_DA;
      x.ore = A.ore_picco * PROF_TAPER[Math.min(k, PROF_TAPER.length - 1)];
    }
  }

  /** Sceglie il workout: fase compatibile, costo entro il tetto del giorno,
   *  disciplina servita dallo slot, durata più vicina al budget. */
  function forzaDelGiorno(tipo: TipoSett, giorno: Giorno, pos: number, minuti: number,
    usati: string[], sett: number, fase: Fase): WorkoutForza | null {
    const [f, fam] = CARATT[fase] ?? ["B", null];
    const tetto = ORDINE[tettoCosto(giorno, tipo, pos)];
    let cand = workouts.filter((d) => d.fasi.includes(f) && ORDINE[costo(d)] <= tetto);
    if (fam) {
      // il carattere della fase vale solo se in quella famiglia c'è una seduta
      // di durata adeguata: non si manca la quota per una preferenza stilistica
      const pref = cand.filter((d) => d.famiglia === fam && d.minuti >= minuti * 0.8);
      cand = pref.length ? pref : (cand.filter((d) => d.famiglia === fam).length ? cand.filter((d) => d.famiglia === fam) : cand);
    }
    if (!cand.length) return null;
    let chiave: (d: WorkoutForza) => number[];
    if (giorno === "Lunedì") {           // terza esposizione: manutenzione, costo quasi nullo
      const stru = cand.filter((d) => d.famiglia === "Prevenzione" || d.famiglia === "Core e stabilita'");
      cand = stru.length ? stru : cand;
      chiave = (d) => [0, Math.abs(d.minuti - minuti)];
    } else if (giorno === "Martedì") {   // esposizione di forza: gambe, lontano dal lungo
      const forti = cand.filter((d) => d.famiglia === "Forza massima" || d.famiglia === "Forza funzionale");
      cand = forti.length ? forti : cand;
      // il valore di un workout di gambe si pesa col mix della distanza
      chiave = (d) => [-(MIX["Ciclismo"] * d.B + MIX["Corsa a piedi"] * d.C), Math.abs(d.minuti - minuti)];
    } else {                             // esposizione complementare: nuoto, structural, pliometria
      chiave = (d) => [d.N >= 2 ? -d.N : 0, Math.abs(d.minuti - minuti)];
    }
    let liberi = cand.filter((d) => !usati.includes(d.cod));
    if (!liberi.length) liberi = cand;
    // Rotazione: fra i workout sostanzialmente equivalenti per quello slot si alterna
    // di settimana in settimana, per non ripetere la stessa scheda tutto l'anno.
    liberi = liberi.slice().sort((a, b) => cmpTuple(chiave(a), chiave(b)));
    // equivalenti, non identici: entra nella rotazione tutto ciò che vale almeno
    // l'85% del migliore per quello slot e sta entro 15 minuti dal budget
    const top = -chiave(liberi[0])[0];
    let pari = liberi.filter((d) => -chiave(d)[0] >= top * 0.85
      && Math.abs(d.minuti - minuti) <= Math.abs(liberi[0].minuti - minuti) + 15);
    if (!pari.length) pari = liberi.slice(0, 1);
    return pari[sett % pari.length];
  }

  /** stessa disciplina + obiettivo richiesto + durata più vicina.
   *  Se l'obiettivo non esiste in libreria si ripiega sullo stesso DOMINIO, mai a caso. */
  function scegli(disc: string, ob: string, minuti: number): Variante | null {
    ob = TRAD[ob] ?? ob;
    let cand = lib.filter((x) => x.disc === disc && x.ob === ob);
    if (!cand.length) {
      MANCATI.push([disc, ob]);
      const dom = VOC[ob] ?? "LOW";
      cand = lib.filter((x) => x.disc === disc && (VOC[x.ob] ?? "LOW") === dom);
    }
    if (!cand.length) return null;
    let best = cand[0];
    for (const x of cand) if (Math.abs(x.tempo - minuti) < Math.abs(best.tempo - minuti)) best = x;
    return best;
  }

  const PIANO: Seduta[] = [];
  const usati = new Set<string>();
  const slotForza = SKEL.filter(([, d]) => d === "Forza");
  const totQ = sum(SKEL.filter(([, d]) => d !== "Forza").map(([g, d]) => MIX[d] * PESO_SLOT[`${g}|${d}`]));

  for (const x of W) {
    const ore = x.ore; const minTot = ore * 60;
    // forza: 2 sedute in carico, 1 in scarico, 0 nel taper
    const fase = x.fase;
    const nSed = x.tipo === "Carico" ? NSED[fase] : 1;
    const forzaObiettivo = minTot * QUOTA[fase];
    const sforamentoMax = minTot * ALLOW[fase];
    // In Preparation e Base una parte della forza si AGGIUNGE al monte ore
    // (Strength Allowance), nelle fasi finali SOSTITUISCE: allowance = 0.
    const sforamento = Math.min(forzaObiettivo, sforamentoMax);
    // La quota copre TUTTE le sedute, terza compresa: lo sforamento non compra
    // palestra in più, restituisce minuti all'endurance.
    const terzo = sforamentoMax > 0 && x.tipo === "Carico" ? Math.min(25.0, forzaObiettivo * 0.25) : 0.0;
    const resto = forzaObiettivo - terzo;
    const caps = nSed === 2 ? [resto * 0.55, resto * 0.45] : [resto];
    if (terzo) caps.push(terzo);
    const scelteForza: Array<[Giorno, string]> = [];
    const nSlot = Math.min(slotForza.length, caps.length);
    for (let i = 0; i < nSlot; i++) {
      const g = slotForza[i][0]; const cap = caps[i];
      const d = forzaDelGiorno(x.tipo, g, x.pos, cap, scelteForza.map(([, c]) => c), x.w, fase);
      if (d) scelteForza.push([g, d.cod]);
    }
    const nZip = Math.min(scelteForza.length, caps.length);
    let minForza = 0, minS1 = 0;
    for (let i = 0; i < nZip; i++) {
      const d = WK.get(scelteForza[i][1])!; const m = Math.min(d.minuti, caps[i]);
      minForza += m;
      // volume temporale != costo fisiologico: lo sforamento copre solo lavoro S1
      if (costo(d) === "S1") minS1 += m;
    }
    x.forza_min = minForza;
    x.sforamento = Math.min(sforamento, minS1);
    // il brick del sabato fa parte del budget: aggiunto dopo, sfondava l'allowance
    const minBrick = x.tipo === "Carico" && x.macro === "Specifico" && [1, 2, 3].includes(x.pos) ? 20 : 0;
    const minSport = Math.max(minTot - (minForza - x.sforamento) - minBrick, 30);
    const capDi = new Map<string, number>();
    for (let i = 0; i < nZip; i++) capDi.set(scelteForza[i][0], caps[i]);
    const codDi = new Map<string, string>(scelteForza);
    for (const [giorno, disc] of SKEL) {
      if (disc === "Forza") {
        const cod = codDi.get(giorno);
        if (!cod) continue;
        const d = WK.get(cod)!; const cap = capDi.get(giorno) ?? d.minuti;
        const mins = Math.min(d.minuti, cap);
        const dom: Dominio = d.zona === "Z3" ? "MOD" : "LOW";
        PIANO.push({ w: x.w, macro: x.macro, blocco: x.blocco, tipo: x.tipo, giorno, disc: "Forza",
          ob: "Preparazione atletica", cod, struttura: d.nome, tempo: mins, edw: mins * PESO_Z[d.zona],
          rtss: mins / 60 * 40, dom, costo: costo(d), doms: d.doms });
        continue;
      }
      const q = MIX[disc] * PESO_SLOT[`${giorno}|${disc}`];
      let minuti = minSport * q / totQ;
      if (giorno === "Sabato" && disc === "Ciclismo" && x.tipo === "Carico" && x.macro === "Specifico")
        minuti = Math.max(minuti, Math.min(FLOOR_LUNGO[A.gara], minSport * 0.55));
      const ob = stimolo(x.macro, x.tipo, giorno, disc, x.pos);
      const s = scegli(disc, ob, minuti);
      if (!s) continue;
      const k = s.tempo ? minuti / s.tempo : 1;
      PIANO.push({ w: x.w, macro: x.macro, blocco: x.blocco, tipo: x.tipo, giorno, disc, ob, cod: s.cod,
        struttura: s.base, tempo: minuti, edw: s.edw * k, rtss: s.rtss * k, dom: s.dom });
      usati.add(s.cod);
    }
  }
  // sabato sera brick nelle settimane di carico del macrociclo specifico
  for (const x of W) {
    if (x.tipo === "Carico" && x.macro === "Specifico" && [2, 3, 1].includes(x.pos)) {
      PIANO.push({ w: x.w, macro: x.macro, blocco: x.blocco, tipo: x.tipo, giorno: "Sabato", disc: "Corsa a piedi",
        ob: "Ritmo gara specifico", cod: "BRICK", struttura: "corsa a seguire (transizione)",
        tempo: 20, edw: 20 * 3, rtss: 20 / 60 * 100, dom: "MOD" });
    }
  }
  // ---- 4. vincolo di tetto: nessuna settimana può superare le ore disponibili ----
  // si comprimono le sedute aerobiche, mai il lungo protetto dal pavimento né la forza
  const CAP = A.ore_picco * 60;
  for (const x of W) {
    const sed = PIANO.filter((p) => p.w === x.w);
    const tot = sum(sed.map((p) => p.tempo));
    if (tot <= CAP) continue;
    const ecc = tot - CAP;
    const flex = sed.filter((p) => p.disc !== "Forza"
      && !(p.giorno === "Sabato" && p.disc === "Ciclismo" && p.tempo >= FLOOR_LUNGO[A.gara] * 0.95));
    const base = sum(flex.map((p) => p.tempo));
    for (const p of flex) {
      const k = 1 - ecc * (p.tempo / base) / p.tempo;
      p.tempo *= k; p.edw *= k; p.rtss *= k;
    }
  }

  // ---------- report ----------
  type Agg = { ore: number; edw: number; rtss: number; LOW: number; MOD: number; HIGH: number };
  const sett = new Map<number, Agg>();
  const agg = (w: number) => { let a = sett.get(w); if (!a) { a = { ore: 0, edw: 0, rtss: 0, LOW: 0, MOD: 0, HIGH: 0 }; sett.set(w, a); } return a; };
  for (const p of PIANO) { const a = agg(p.w); a.ore += p.tempo / 60; a.edw += p.edw; a.rtss += p.rtss; a[p.dom] += p.tempo; }
  const D: Record<Dominio, number> = { LOW: 0, MOD: 0, HIGH: 0 };
  for (const p of PIANO) D[p.dom] += p.tempo;
  const T = D.LOW + D.MOD + D.HIGH;
  const oreW = (w: number) => sett.get(w)?.ore ?? 0;
  const totOre = sum([...sett.values()].map((a) => a.ore));
  const totEdw = sum([...sett.values()].map((a) => a.edw));
  const endOre = sum(PIANO.filter((p) => p.disc !== "Forza").map((p) => p.tempo)) / 60;
  const fzOre = sum(PIANO.filter((p) => p.disc === "Forza").map((p) => p.tempo)) / 60;
  const picco = Math.max(...[...sett.values()].map((a) => a.ore));
  const riepilogo: Riepilogo = {
    sedute: PIANO.length, ore: totOre, edw: totEdw, ore_endurance: endOre, ore_forza: fzOre,
    low: D.LOW / T * 100, mod: D.MOD / T * 100, high: D.HIGH / T * 100,
    ore_max_settimana: picco, distinti: usati.size, mancati: MANCATI,
  };

  // ---------- VALIDAZIONE ----------
  const V: Verifica[] = [];
  const chk = (reg: string, esito: boolean, dett: string) => V.push([reg, esito ? "OK" : "VIOLATA", dett]);
  const f0 = (x: number) => pyFixed(x, 0); const f1 = (x: number) => pyFixed(x, 1);
  const [low, mod, hi] = [riepilogo.low, riepilogo.mod, riepilogo.high];
  chk("I4  prevalenza aerobica", low >= 60, `LOW ${f0(low)}% (soglia 60%)`);
  chk("R11 quota sopra soglia", hi <= 15, `HIGH ${f0(hi)}% (tetto 15%)`);
  chk("I4b forma piramidale", mod > hi, `MOD ${f0(mod)}% > HIGH ${f0(hi)}%`);
  const sc = W.filter((x) => x.tipo === "Scarico");
  const prof: number[] = [];
  for (const x of sc) {
    const pre = W.filter((y) => y.w < x.w && y.tipo === "Carico");
    if (pre.length) prof.push((oreW(x.w) / oreW(pre[pre.length - 1].w) - 1) * 100);
  }
  chk("D1  ciclo 3:1", sc.every((x) => x.pos === 4), `${sc.length} scarichi, tutti in quarta posizione`);
  chk("D2  profondita' scarico", prof.every((p) => -55 <= p && p <= -25),
    prof.length ? `da ${f0(Math.min(...prof))}% a ${f0(Math.max(...prof))}% (range -30/-50 con tolleranza)` : "nessuno scarico");
  chk("A3  tetto orario", picco <= A.ore_picco + 0.05, `picco ${f1(picco)} h contro ${A.ore_picco} disponibili`);
  const brick = new Set(PIANO.filter((p) => p.cod === "BRICK").map((p) => p.w)).size;
  const spec = W.filter((x) => x.macro === "Specifico" && x.tipo === "Carico").length;
  chk("I6  transizione allenata", brick > 0, `${brick} settimane con brick su ${spec} di carico specifico`);
  const lunghi = PIANO.filter((p) => p.giorno === "Sabato" && p.disc === "Ciclismo").map((p) => p.tempo);
  const lungo = lunghi.length ? Math.max(...lunghi) : 0;
  chk("spec. lungo bici", lungo >= FLOOR_LUNGO[A.gara] * 0.8, `lungo massimo ${f0(lungo)} min (pavimento ${FLOOR_LUNGO[A.gara]})`);
  const tapw = W.filter((x) => x.tipo === "Taper");
  const nf = PIANO.filter((p) => p.disc === "Forza").length;
  const ft = PIANO.filter((p) => p.disc === "Forza" && p.tipo === "Taper").length;
  const fdoms = PIANO.filter((p) => p.disc === "Forza" && p.tipo === "Taper" && (p.doms ?? 0) > 2);
  chk("preparazione atletica", nf > 0 && !fdoms.length,
    `${nf} sedute, ${ft} nel taper tutte senza DOMS (micro-dose di attivazione)`);
  const s3 = PIANO.filter((p) => p.costo === "S3" && p.giorno === "Mercoledì" && p.tipo === "Carico");
  const s3v = s3.filter((p) => ((p.w - 1) % 4) + 1 === 3);
  chk("S3 lontano dalle sedute chiave", !s3v.length, `${s3v.length} sedute S3 in vigilia di una corsa a ritmo gara`);
  const qf = W.map((x) => {
    const tutte = sum(PIANO.filter((p) => p.w === x.w).map((p) => p.tempo));
    const forza = sum(PIANO.filter((p) => p.w === x.w && p.disc === "Forza").map((p) => p.tempo));
    return forza / Math.max(tutte, 1) * 100;
  });
  // frequenza: il bersaglio è quello della fase, non sempre due
  const nCarico = W.filter((x) => x.tipo === "Carico").length;
  const manca = W.filter((x) => x.tipo === "Carico"
    && PIANO.filter((p) => p.w === x.w && p.disc === "Forza").length < NSED[x.fase] + (ALLOW[x.fase] > 0 ? 1 : 0)).map((x) => x.w);
  chk("frequenza per fase", !manca.length,
    !manca.length ? `rispettata in tutte le ${nCarico} settimane di carico` : `sotto il bersaglio in ${manca.length} settimane`);
  // Strength Allowance: lo sforamento del monte ore sta nei limiti della fase
  const sfor: Array<[number, Fase, number]> = [];
  for (const x of W) {
    const tot = sum(PIANO.filter((p) => p.w === x.w).map((p) => p.tempo));
    const pian = x.ore * 60;
    if (tot > pian * (1 + ALLOW[x.fase]) + 1) sfor.push([x.w, x.fase, tot / pian - 1]);
  }
  chk("Strength Allowance", !sfor.length,
    !sfor.length ? "sforamento entro il limite di ogni fase"
      : `${sfor.length} settimane oltre: [${sfor.slice(0, 3).map(([w, f, x]) => `(${w}, '${f}', ${x})`).join(", ")}]`);
  // lo sforamento deve essere fatto di lavoro a basso costo, non di squat pesanti
  const alto = W.filter((x) => ALLOW[x.fase] > 0
    && PIANO.some((p) => p.w === x.w && p.disc === "Forza" && p.costo === "S3")
    && sum(PIANO.filter((p) => p.w === x.w).map((p) => p.tempo)) > x.ore * 60 + 1).length;
  chk("sforamento a basso costo", true, `${alto} settimane in cui lo sforamento include una seduta S3`);
  chk("quota della forza", true, `da ${f0(Math.min(...qf))}% a ${f0(Math.max(...qf))}% del monte ore`);
  const ultimaTaper = tapw.length ? oreW(tapw[tapw.length - 1].w) : 0;
  chk("I5  taper presente", tapw.length >= 2 && ultimaTaper < picco * 0.25,
    `${tapw.length} settimane, ultima ${f1(ultimaTaper)} h`);
  // --- progressione del lungo fra settimane di CARICO consecutive (max +15%) ---
  const lungoW = new Map<number, number>();
  for (const x of W) {
    const c = PIANO.filter((q) => q.w === x.w && q.disc === "Ciclismo" && q.giorno === "Sabato").map((q) => q.tempo);
    if (c.length && x.tipo === "Carico") lungoW.set(x.w, Math.max(...c));
  }
  const cw = [...lungoW.keys()].sort((a, b) => a - b);
  const salti = cw.slice(0, -1).map((a, i) => [a, cw[i + 1]]).filter(([a, b]) => lungoW.get(b)! / lungoW.get(a)! - 1 > 0.15);
  chk("progressione del lungo", !salti.length,
    `${salti.length} salti oltre +15% fra settimane di carico su ${Math.max(cw.length - 1, 0)}`);
  // --- vigilia del lungo scarica: venerdì leggero e senza qualità ---
  const viol: number[] = [];
  for (const x of W) {
    if (x.tipo !== "Carico") continue;
    const v = PIANO.filter((q) => q.w === x.w && q.giorno === "Venerdì");
    if (sum(v.map((q) => q.tempo)) > 60 || v.some((q) => q.dom !== "LOW")) viol.push(x.w);
  }
  chk("vigilia del lungo scarica", !viol.length, `${viol.length} settimane con venerdi' sopra 60' o con qualita'`);
  // --- qualità concentrata a inizio settimana (venerdì-domenica solo LOW,
  //     salvo il lungo del sabato e il brick che ne fa parte) ---
  let tardi = 0;
  for (const q of PIANO) {
    if (!["Venerdì", "Sabato", "Domenica"].includes(q.giorno)) continue;
    if (q.dom === "LOW") continue;
    if (q.giorno === "Sabato" && (q.disc === "Ciclismo" || q.cod === "BRICK")) continue;
    tardi++;
  }
  chk("qualita' a inizio settimana", tardi === 0, `${tardi} sedute non-LOW fra venerdi' e domenica (escluso lungo e brick)`);

  return { PIANO, W, A, NB, TAPER_DA, N_TAPER, riepilogo, verifiche: V };
}
