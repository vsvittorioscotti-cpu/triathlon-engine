/** Livello 1 — la scala (I8): decide QUALE gradino è raggiungibile, poi quante
 *  settimane spettano a ciascun blocco applicando E7. Il livello 2
 *  (generatore.ts) lavora solo su ciò che questo modulo gli lascia.
 *  Porting 1:1 di scala_gen.py. */
import { pyFixed, pyRound } from "./py";

export type Gradino = "Triathlon Sprint" | "Triathlon Olimpico" | "Half-Ironman" | "Ironman";

/** gradino, settimane naturali del blocco, ore di picco, ore medie
 *  (dal libro, con le soglie ancorate: vedi scala2.py) */
export const SCALA: ReadonlyArray<readonly [Gradino, number, number, number]> = [
  ["Triathlon Sprint", 8, 7.5, 6.1],
  ["Triathlon Olimpico", 16, 19.6, 12.8],
  ["Half-Ironman", 8, 19.0, 14.3],
  ["Ironman", 12, 27.0, 18.7],
];
export const NOMI: Gradino[] = SCALA.map((g) => g[0]);

export const TRANSIZIONE = 2;   // settimane di recupero dopo ogni gara   (DEFAULT)
export const INTRO = 4;         // introduzione per chi parte da zero     (DEFAULT)
export const RITENZIONE = 0.85; // quota del picco che si porta al blocco dopo (HEURISTIC)
export const PEND_MIN = 0.05;   // E4: pendenza settimanale minima utile
export const QUOTA_MIN = 0.5;   // E3: partenza minima come quota del picco

export interface Blocco {
  gradino: Gradino;
  settimane: number;
  naturali: number;
  riempimento: number;
  picco: number;
  ore_inizio: number;
  sat: number;
}

export interface PianoScala {
  gradino_fatto: string;
  obiettivo: Gradino;
  ore_disponibili: number;
  tetto_rigido: boolean;
  arrivo: Gradino;
  raggiunge_obiettivo: boolean;
  vincolo: string;
  intro: number;
  blocchi: Blocco[];
  transizioni: number;
  non_assorbite: number;
  settimane_disponibili: number;
  settimane_usate: number;
}

export interface ErroreScala {
  errore: string;
  gradino_prossimo?: Gradino;
  settimane_necessarie?: number;
  settimane_disponibili?: number;
  ore_necessarie?: number;
  ore_disponibili?: number;
}

export type RisultatoScala = PianoScala | ErroreScala;
export const isErrore = (r: RisultatoScala): r is ErroreScala => "errore" in r;

export interface Fabbisogno {
  gradino: Gradino;
  picco: number;
  settimana: number;
  serve_in_piu: number;
  gia_coperto: boolean;
  disp_al_momento: number;
  tipo: "costruzione" | "specificita' a volume quasi costante";
  pendenza: number;
  pendenza_ok: boolean;
}

/** (regola, esito, dettaglio) */
export type Verifica = [string, "OK" | "VIOLATA", string];

export function idxGradino(fatto: string | null | undefined): number {
  return fatto && (NOMI as string[]).includes(fatto) ? (NOMI as string[]).indexOf(fatto) : -1;
}

/** settimane per salire dai gradini i0+1..i1 compresi, transizioni incluse */
function settNaturali(i0: number, i1: number, daZero: boolean): number {
  let n = daZero ? INTRO : 0;
  for (let k = i0 + 1; k <= i1; k++) {
    n += SCALA[k][1];
    if (k < i1) n += TRANSIZIONE; // gara + recupero fra un gradino e l'altro
  }
  return n;
}

/** E3/E4: quante settimane di CARICO una rampa può contenere restando utile */
export function caricoMax(oreInizio: number, orePicco: number): number {
  if (oreInizio <= 0 || orePicco <= oreInizio) return 3;
  oreInizio = Math.max(oreInizio, orePicco * QUOTA_MIN); // E3
  return 1 + Math.log(orePicco / oreInizio) / Math.log(1 + PEND_MIN); // E4
}

export function livelloScala(
  gradinoFatto: string | null | undefined,
  settimane: number,
  oreDisponibili: number,
  oreOggi: number,
  obiettivo: Gradino = "Ironman",
  tettoRigido = false,
): RisultatoScala {
  const i0 = idxGradino(gradinoFatto);
  const daZero = i0 < 0;
  const iObiettivo = NOMI.indexOf(obiettivo);
  if (iObiettivo <= i0) return { errore: `${obiettivo} e' un gradino gia' completato` };

  // cancello ORE. La disponibilità dichiarata è un punto di partenza, non un
  // muro: può restare uguale o crescere. Blocca solo se dichiarata come tetto
  // rigido; altrimenti diventa un FABBISOGNO che il piano mette in conto.
  let tettoI: number;
  if (tettoRigido) {
    tettoI = i0;
    for (let k = i0 + 1; k <= iObiettivo; k++) {
      if (SCALA[k][2] <= oreDisponibili) tettoI = k;
      else break;
    }
  } else tettoI = iObiettivo;
  // cancello TEMPO
  let tempoI = i0;
  for (let k = i0 + 1; k <= iObiettivo; k++) {
    if (settNaturali(i0, k, daZero) <= settimane) tempoI = k;
    else break;
  }

  const arrivo = Math.min(tettoI, tempoI);
  if (arrivo <= i0) {
    return {
      errore: "nemmeno il primo gradino e' raggiungibile",
      gradino_prossimo: NOMI[i0 + 1],
      settimane_necessarie: settNaturali(i0, i0 + 1, daZero),
      settimane_disponibili: settimane,
      ore_necessarie: SCALA[i0 + 1][2],
      ore_disponibili: oreDisponibili,
    };
  }

  let vincolo: string;
  if (arrivo === iObiettivo) vincolo = "nessuno: obiettivo raggiungibile";
  else {
    const quali: string[] = [];
    if (tettoI === arrivo) quali.push("ore");
    if (tempoI === arrivo) quali.push("tempo");
    vincolo = quali.join(" e ");
  }

  // ---- E7: il surplus si assorbe, non si attende ----
  const blocchi: Blocco[] = [];
  let inizio = oreOggi;
  for (let k = i0 + 1; k <= arrivo; k++) {
    const [nome, nat, picco] = SCALA[k];
    blocchi.push({
      gradino: nome, settimane: nat, naturali: nat, riempimento: 0, picco,
      ore_inizio: pyRound(inizio, 1), sat: caricoMax(inizio, picco),
    });
    inizio = picco * RITENZIONE;
  }
  const surplus = settimane - settNaturali(i0, arrivo, daZero);
  let resto = surplus % 4;
  let unita = Math.floor(surplus / 4);
  while (unita > 0) {
    let assorbita = false;
    for (const b of blocchi) {                                   // dal basso verso l'alto (E7.2)
      if (b === blocchi[blocchi.length - 1] && blocchi.length > 1) continue; // il più alto mai (E7.5)
      if ((b.settimane + 4) * 0.75 <= b.sat) {                   // E3/E4 (E7.3)
        b.settimane += 4; b.riempimento += 4;
        unita -= 1; assorbita = true;
        break;
      }
    }
    if (!assorbita) {                 // tutti saturi: nessuna unità va persa
      resto += 4 * unita;
      unita = 0;
    }
  }
  const sommaBlocchi = blocchi.reduce((s, b) => s + b.settimane, 0);
  return {
    gradino_fatto: gradinoFatto || "nessuno",
    obiettivo,
    ore_disponibili: oreDisponibili,
    tetto_rigido: tettoRigido,
    arrivo: NOMI[arrivo],
    raggiunge_obiettivo: arrivo === iObiettivo,
    vincolo,
    intro: daZero ? INTRO : 0,
    blocchi,
    transizioni: TRANSIZIONE * (blocchi.length - 1),
    non_assorbite: resto,
    settimane_disponibili: settimane,
    settimane_usate: (daZero ? INTRO : 0) + sommaBlocchi + TRANSIZIONE * (blocchi.length - 1) + resto,
  };
}

/** Per ogni blocco: picco richiesto, settimana in cui cade, crescita implicita
 *  rispetto alla disponibilità dichiarata oggi. */
export function fabbisognoOre(p: PianoScala): Fabbisogno[] {
  const out: Fabbisogno[] = [];
  let w = p.intro;
  let disp = p.ore_disponibili;
  for (const b of p.blocchi) {
    const wPicco = w + b.settimane - 2; // il picco cade prima del taper
    const settCarico = Math.ceil(b.settimane * 0.75);
    const pend = Math.pow(b.picco / Math.max(b.ore_inizio, 0.1), 1 / Math.max(settCarico - 1, 1)) - 1;
    // un blocco il cui picco non supera il volume già raggiunto non costruisce
    // volume: converte volume in specificità. E4 non si applica come violazione.
    const tipo = pend >= PEND_MIN ? "costruzione" : "specificita' a volume quasi costante";
    out.push({
      gradino: b.gradino, picco: b.picco, settimana: wPicco,
      serve_in_piu: pyRound(Math.max(0, b.picco - disp), 1),
      gia_coperto: b.picco <= disp, disp_al_momento: pyRound(disp, 1),
      tipo, pendenza: pend, pendenza_ok: pend <= 0.15,
    });
    disp = Math.max(disp, b.picco);
    w += b.settimane + TRANSIZIONE;
  }
  return out;
}

/** undicesima verifica: la scala non si salta e non si supera */
export function verificaI8(p: PianoScala, gradinoFatto: string | null | undefined, obiettivo: Gradino): Verifica[] {
  const V: Verifica[] = [];
  const chk = (reg: string, ok: boolean, dett: string) => V.push([reg, ok ? "OK" : "VIOLATA", dett]);
  const i0 = idxGradino(gradinoFatto);
  const attesi = NOMI.slice(i0 + 1, NOMI.indexOf(p.arrivo) + 1);
  const ottenuti = p.blocchi.map((b) => b.gradino);
  chk("I8  nessun gradino saltato", JSON.stringify(ottenuti) === JSON.stringify(attesi),
    ottenuti.length ? ottenuti.join(" -> ") : "nessuno");
  chk("I8b arrivo non oltre il raggiungibile", NOMI.indexOf(p.arrivo) <= NOMI.indexOf(obiettivo), `arrivo ${p.arrivo}`);
  const senzaUltimo = p.blocchi.length > 1 ? p.blocchi.slice(0, -1) : p.blocchi;
  chk("E7  nulla di assorbibile e' rimasto fuori",
    p.non_assorbite < 4 || senzaUltimo.every((b) => (b.settimane + 4) * 0.75 > b.sat),
    `${p.non_assorbite} settimane non assorbite`);
  const ultimo = p.blocchi[p.blocchi.length - 1];
  chk("E7b il gradino piu' alto non e' riempito",
    p.blocchi.length === 1 || ultimo.riempimento === 0,
    p.blocchi.length === 1
      ? "un solo blocco: e' anche il piu' basso, il riempimento gli spetta"
      : `riempimento sul piu' alto: ${ultimo.riempimento} sett.`);
  const piccoMax = Math.max(...p.blocchi.map((b) => b.picco));
  chk("A3  ore richieste da ogni blocco",
    !p.tetto_rigido || p.blocchi.every((b) => b.picco <= p.ore_disponibili),
    `picco massimo ${pyFixed(piccoMax, 1)} h contro ${p.ore_disponibili} dichiarate`
      + (p.tetto_rigido ? "" : " (tetto non rigido: e' un fabbisogno)"));
  chk("E7c il residuo sta dentro una transizione", p.non_assorbite < 4,
    `${p.non_assorbite} settimane fuori dai blocchi`
      + (p.non_assorbite >= 4 ? " -> periodo non coperto dalla dottrina" : ""));
  return V;
}
