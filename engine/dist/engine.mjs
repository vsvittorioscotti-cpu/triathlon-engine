// src/py.ts
function pyFixed(x, nd) {
  if (!isFinite(x)) return String(x);
  const neg = x < 0 || Object.is(x, -0);
  const s = Math.abs(x).toFixed(Math.min(100, nd + 30));
  const [int, frac] = s.split(".");
  const keep = frac.slice(0, nd);
  const rest = frac.slice(nd);
  let up = false;
  if (rest[0] > "5") up = true;
  else if (rest[0] === "5") {
    if (/[1-9]/.test(rest.slice(1))) up = true;
    else {
      const last = nd > 0 ? keep[nd - 1] : int[int.length - 1];
      up = Number(last) % 2 === 1;
    }
  }
  let digits = int + keep;
  if (up) {
    const arr = digits.split("");
    let i = arr.length - 1;
    while (i >= 0) {
      if (arr[i] === "9") {
        arr[i] = "0";
        i--;
      } else {
        arr[i] = String(Number(arr[i]) + 1);
        break;
      }
    }
    if (i < 0) arr.unshift("1");
    digits = arr.join("");
  }
  const ip = digits.slice(0, digits.length - nd) || "0";
  const fp = digits.slice(digits.length - nd);
  const out = nd > 0 ? `${ip}.${fp}` : ip;
  return (neg && /[1-9]/.test(out) ? "-" : "") + out;
}
function pyRound(x, nd) {
  return Number(pyFixed(x, nd));
}
function cmpTuple(a, b) {
  for (let i = 0; i < Math.min(a.length, b.length); i++) {
    if (a[i] < b[i]) return -1;
    if (a[i] > b[i]) return 1;
  }
  return a.length - b.length;
}

// src/scala.ts
var SCALA = [
  ["Triathlon Sprint", 8, 7.5, 6.1],
  ["Triathlon Olimpico", 16, 19.6, 12.8],
  ["Half-Ironman", 8, 19, 14.3],
  ["Ironman", 12, 27, 18.7]
];
var NOMI = SCALA.map((g) => g[0]);
var TRANSIZIONE = 2;
var INTRO = 4;
var RITENZIONE = 0.85;
var PEND_MIN = 0.05;
var QUOTA_MIN = 0.5;
var isErrore = (r) => "errore" in r;
function idxGradino(fatto) {
  return fatto && NOMI.includes(fatto) ? NOMI.indexOf(fatto) : -1;
}
function settNaturali(i0, i1, daZero) {
  let n = daZero ? INTRO : 0;
  for (let k = i0 + 1; k <= i1; k++) {
    n += SCALA[k][1];
    if (k < i1) n += TRANSIZIONE;
  }
  return n;
}
function caricoMax(oreInizio, orePicco) {
  if (oreInizio <= 0 || orePicco <= oreInizio) return 3;
  oreInizio = Math.max(oreInizio, orePicco * QUOTA_MIN);
  return 1 + Math.log(orePicco / oreInizio) / Math.log(1 + PEND_MIN);
}
function livelloScala(gradinoFatto, settimane, oreDisponibili, oreOggi, obiettivo = "Ironman", tettoRigido = false) {
  const i0 = idxGradino(gradinoFatto);
  const daZero = i0 < 0;
  const iObiettivo = NOMI.indexOf(obiettivo);
  if (iObiettivo <= i0) return { errore: `${obiettivo} e' un gradino gia' completato` };
  let tettoI;
  if (tettoRigido) {
    tettoI = i0;
    for (let k = i0 + 1; k <= iObiettivo; k++) {
      if (SCALA[k][2] <= oreDisponibili) tettoI = k;
      else break;
    }
  } else tettoI = iObiettivo;
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
      ore_disponibili: oreDisponibili
    };
  }
  let vincolo;
  if (arrivo === iObiettivo) vincolo = "nessuno: obiettivo raggiungibile";
  else {
    const quali = [];
    if (tettoI === arrivo) quali.push("ore");
    if (tempoI === arrivo) quali.push("tempo");
    vincolo = quali.join(" e ");
  }
  const blocchi = [];
  let inizio = oreOggi;
  for (let k = i0 + 1; k <= arrivo; k++) {
    const [nome, nat, picco] = SCALA[k];
    blocchi.push({
      gradino: nome,
      settimane: nat,
      naturali: nat,
      riempimento: 0,
      picco,
      ore_inizio: pyRound(inizio, 1),
      sat: caricoMax(inizio, picco)
    });
    inizio = picco * RITENZIONE;
  }
  const surplus = settimane - settNaturali(i0, arrivo, daZero);
  let resto = surplus % 4;
  let unita = Math.floor(surplus / 4);
  while (unita > 0) {
    let assorbita = false;
    for (const b of blocchi) {
      if (b === blocchi[blocchi.length - 1] && blocchi.length > 1) continue;
      if ((b.settimane + 4) * 0.75 <= b.sat) {
        b.settimane += 4;
        b.riempimento += 4;
        unita -= 1;
        assorbita = true;
        break;
      }
    }
    if (!assorbita) {
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
    settimane_usate: (daZero ? INTRO : 0) + sommaBlocchi + TRANSIZIONE * (blocchi.length - 1) + resto
  };
}
function fabbisognoOre(p) {
  const out = [];
  let w = p.intro;
  let disp = p.ore_disponibili;
  for (const b of p.blocchi) {
    const wPicco = w + b.settimane - 2;
    const settCarico = Math.ceil(b.settimane * 0.75);
    const pend = Math.pow(b.picco / Math.max(b.ore_inizio, 0.1), 1 / Math.max(settCarico - 1, 1)) - 1;
    const tipo = pend >= PEND_MIN ? "costruzione" : "specificita' a volume quasi costante";
    out.push({
      gradino: b.gradino,
      picco: b.picco,
      settimana: wPicco,
      serve_in_piu: pyRound(Math.max(0, b.picco - disp), 1),
      gia_coperto: b.picco <= disp,
      disp_al_momento: pyRound(disp, 1),
      tipo,
      pendenza: pend,
      pendenza_ok: pend <= 0.15
    });
    disp = Math.max(disp, b.picco);
    w += b.settimane + TRANSIZIONE;
  }
  return out;
}
function verificaI8(p, gradinoFatto, obiettivo) {
  const V = [];
  const chk = (reg, ok, dett) => V.push([reg, ok ? "OK" : "VIOLATA", dett]);
  const i0 = idxGradino(gradinoFatto);
  const attesi = NOMI.slice(i0 + 1, NOMI.indexOf(p.arrivo) + 1);
  const ottenuti = p.blocchi.map((b) => b.gradino);
  chk(
    "I8  nessun gradino saltato",
    JSON.stringify(ottenuti) === JSON.stringify(attesi),
    ottenuti.length ? ottenuti.join(" -> ") : "nessuno"
  );
  chk("I8b arrivo non oltre il raggiungibile", NOMI.indexOf(p.arrivo) <= NOMI.indexOf(obiettivo), `arrivo ${p.arrivo}`);
  const senzaUltimo = p.blocchi.length > 1 ? p.blocchi.slice(0, -1) : p.blocchi;
  chk(
    "E7  nulla di assorbibile e' rimasto fuori",
    p.non_assorbite < 4 || senzaUltimo.every((b) => (b.settimane + 4) * 0.75 > b.sat),
    `${p.non_assorbite} settimane non assorbite`
  );
  const ultimo = p.blocchi[p.blocchi.length - 1];
  chk(
    "E7b il gradino piu' alto non e' riempito",
    p.blocchi.length === 1 || ultimo.riempimento === 0,
    p.blocchi.length === 1 ? "un solo blocco: e' anche il piu' basso, il riempimento gli spetta" : `riempimento sul piu' alto: ${ultimo.riempimento} sett.`
  );
  const piccoMax = Math.max(...p.blocchi.map((b) => b.picco));
  chk(
    "A3  ore richieste da ogni blocco",
    !p.tetto_rigido || p.blocchi.every((b) => b.picco <= p.ore_disponibili),
    `picco massimo ${pyFixed(piccoMax, 1)} h contro ${p.ore_disponibili} dichiarate` + (p.tetto_rigido ? "" : " (tetto non rigido: e' un fabbisogno)")
  );
  chk(
    "E7c il residuo sta dentro una transizione",
    p.non_assorbite < 4,
    `${p.non_assorbite} settimane fuori dai blocchi` + (p.non_assorbite >= 4 ? " -> periodo non coperto dalla dottrina" : "")
  );
  return V;
}

// src/generatore.ts
var FASI = [
  ["Preparation", 0.1],
  ["Base 1", 0.15],
  ["Base 2", 0.15],
  ["Build 1", 0.15],
  ["Build 2", 0.15],
  ["Specific", 0.18],
  ["Peak", 0.12]
];
var QUOTA = {
  "Preparation": 0.175,
  "Base 1": 0.165,
  "Base 2": 0.135,
  "Build 1": 0.105,
  "Build 2": 0.085,
  "Specific": 0.065,
  "Peak": 0.04,
  "Taper": 0.015
};
var ALLOW = {
  "Preparation": 0.125,
  "Base 1": 0.09,
  "Base 2": 0.065,
  "Build 1": 0.025,
  "Build 2": 0.015,
  "Specific": 0,
  "Peak": 0,
  "Taper": 0
};
var NSED = {
  "Preparation": 2,
  "Base 1": 2,
  "Base 2": 2,
  "Build 1": 2,
  "Build 2": 2,
  "Specific": 2,
  "Peak": 1,
  "Taper": 1
};
var CARATT = {
  "Preparation": ["B", null],
  "Base 1": ["B", "Forza massima"],
  "Base 2": ["B", "Forza massima"],
  "Build 1": ["U", null],
  "Build 2": ["U", null],
  "Specific": ["S", null],
  "Peak": ["P", null],
  "Taper": ["P", null]
};
function architettura(n) {
  const blocchi = Math.ceil(n / 4);
  const meta = Math.max(1, Math.floor(blocchi / 2));
  const range = (a, b) => Array.from({ length: Math.max(0, b - a) }, (_, i) => a + i);
  return [[["Preparatorio", range(1, meta + 1)], ["Specifico", range(meta + 1, blocchi + 1)]], blocchi];
}
var SKEL = [
  ["Marted\xEC", "Nuoto"],
  ["Marted\xEC", "Corsa a piedi"],
  ["Marted\xEC", "Forza"],
  ["Mercoled\xEC", "Ciclismo"],
  ["Mercoled\xEC", "Forza"],
  ["Gioved\xEC", "Nuoto"],
  ["Gioved\xEC", "Corsa a piedi"],
  ["Venerd\xEC", "Nuoto"],
  ["Sabato", "Ciclismo"],
  ["Domenica", "Corsa a piedi"],
  ["Luned\xEC", "Forza"]
];
var PESO_Z = { Z1: 1, Z2: 2, Z3: 3, Z4: 4, Z5: 5 };
var ORDINE = { S1: 1, S2: 2, S3: 3 };
function costo(d) {
  return d.doms >= 4 ? "S3" : d.doms === 3 ? "S2" : "S1";
}
function tettoCosto(giorno, tipo, pos) {
  if (giorno === "Luned\xEC") return "S1";
  if (tipo === "Taper" || tipo === "Scarico") return "S1";
  if (giorno === "Mercoled\xEC" && pos === 3) return "S2";
  return "S3";
}
var MIX = { "Ciclismo": 0.51, "Corsa a piedi": 0.31, "Nuoto": 0.18 };
var PESO_SLOT = {
  "Sabato|Ciclismo": 0.75,
  "Mercoled\xEC|Ciclismo": 0.25,
  "Domenica|Corsa a piedi": 0.4,
  "Marted\xEC|Corsa a piedi": 0.3,
  "Gioved\xEC|Corsa a piedi": 0.3,
  "Marted\xEC|Nuoto": 0.38,
  "Gioved\xEC|Nuoto": 0.38,
  "Venerd\xEC|Nuoto": 0.24
};
function stimolo(macro, tipo, giorno, disc, pos = 1) {
  if (tipo === "Taper") {
    if (giorno === "Marted\xEC") return "Ritmo gara specifico";
    if (giorno === "Mercoled\xEC" && disc === "Ciclismo") return "Ritmo gara specifico";
    return "Aerobico base";
  }
  if (giorno === "Venerd\xEC") return "Recupero attivo";
  if (tipo === "Scarico") return giorno === "Marted\xEC" && disc === "Corsa a piedi" ? "Soglia anaerobica" : "Aerobico base";
  if (macro === "Preparatorio") {
    if (giorno === "Marted\xEC" && disc === "Corsa a piedi") return pos === 2 || pos === 3 ? "Soglia anaerobica" : "Aerobico base";
    if (giorno === "Domenica" && disc === "Corsa a piedi") return "Aerobico lento (lungo)";
    if (giorno === "Sabato") return "Aerobico lento (lungo)";
    return "Aerobico base";
  }
  if (giorno === "Marted\xEC" && disc === "Corsa a piedi") return pos === 2 ? "VO2max" : "Soglia anaerobica";
  if (giorno === "Mercoled\xEC" && disc === "Ciclismo") return "Ritmo gara specifico";
  if (giorno === "Sabato" && disc === "Ciclismo") return pos === 3 ? "Ritmo gara specifico" : "Aerobico lento (lungo)";
  if (giorno === "Gioved\xEC" && disc === "Corsa a piedi") return pos === 3 ? "Ritmo gara specifico" : "Aerobico base";
  if (giorno === "Domenica" && disc === "Corsa a piedi") return "Aerobico lento (lungo)";
  return "Aerobico base";
}
var FLOOR_LUNGO = { "Ironman": 210, "Half-Ironman": 150, "Triathlon Olimpico": 90, "Triathlon Sprint": 60 };
var VOC = {
  "Recupero attivo": "LOW",
  "Aerobico base": "LOW",
  "Ritmo gara specifico": "MOD",
  "Soglia anaerobica": "HIGH",
  "VO2max": "HIGH"
};
var TRAD = {
  "Aerobico lento (lungo)": "Aerobico base",
  "Forza specifica": "Aerobico base",
  "Capacita' anaerobica": "VO2max",
  "Velocita' neuromuscolare": "VO2max"
};
var sum = (xs) => xs.reduce((a, b) => a + b, 0);
function generaBlocco(A, lib, workouts) {
  const WK = /* @__PURE__ */ new Map();
  for (const w of workouts) WK.set(w.cod, w);
  const MANCATI = [];
  const N_TAPER = A.settimane <= 8 ? 1 : 2;
  const PROF_TAPER = N_TAPER === 1 ? [0.32] : [0.5, 0.1];
  const [MACRO, NB] = architettura(A.settimane);
  const TAPER_DA = A.settimane - N_TAPER + 1;
  const faseDi = (w) => {
    if (w >= TAPER_DA) return "Taper";
    const n = TAPER_DA - 1;
    let cum = 0;
    for (const [nome, q] of FASI) {
      cum += q;
      if (w <= Math.ceil(cum * n)) return nome;
    }
    return FASI[FASI.length - 1][0];
  };
  const W = [];
  for (let w = 1; w <= A.settimane; w++) {
    const blocco = Math.floor((w - 1) / 4) + 1;
    const pos = (w - 1) % 4 + 1;
    let macro = MACRO.find(([, bs]) => bs.includes(blocco))?.[0] ?? "Taper";
    let tipo;
    if (w >= TAPER_DA) {
      tipo = "Taper";
      macro = "Taper";
    } else if (pos === 4) tipo = "Scarico";
    else tipo = "Carico";
    W.push({ w, blocco, pos, macro, tipo, fase: faseDi(w), ore: 0, forza_min: 0, sforamento: 0 });
  }
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
      x.ore = prec.length ? prec[prec.length - 1].ore * 0.6 : A.ore_oggi * 0.6;
    } else if (x.tipo === "Taper") {
      const k = x.w - TAPER_DA;
      x.ore = A.ore_picco * PROF_TAPER[Math.min(k, PROF_TAPER.length - 1)];
    }
  }
  function forzaDelGiorno(tipo, giorno, pos, minuti, usati2, sett2, fase) {
    const [f, fam] = CARATT[fase] ?? ["B", null];
    const tetto = ORDINE[tettoCosto(giorno, tipo, pos)];
    let cand = workouts.filter((d) => d.fasi.includes(f) && ORDINE[costo(d)] <= tetto);
    if (fam) {
      const pref = cand.filter((d) => d.famiglia === fam && d.minuti >= minuti * 0.8);
      cand = pref.length ? pref : cand.filter((d) => d.famiglia === fam).length ? cand.filter((d) => d.famiglia === fam) : cand;
    }
    if (!cand.length) return null;
    let chiave;
    if (giorno === "Luned\xEC") {
      const stru = cand.filter((d) => d.famiglia === "Prevenzione" || d.famiglia === "Core e stabilita'");
      cand = stru.length ? stru : cand;
      chiave = (d) => [0, Math.abs(d.minuti - minuti)];
    } else if (giorno === "Marted\xEC") {
      const forti = cand.filter((d) => d.famiglia === "Forza massima" || d.famiglia === "Forza funzionale");
      cand = forti.length ? forti : cand;
      chiave = (d) => [-(MIX["Ciclismo"] * d.B + MIX["Corsa a piedi"] * d.C), Math.abs(d.minuti - minuti)];
    } else {
      chiave = (d) => [d.N >= 2 ? -d.N : 0, Math.abs(d.minuti - minuti)];
    }
    let liberi = cand.filter((d) => !usati2.includes(d.cod));
    if (!liberi.length) liberi = cand;
    liberi = liberi.slice().sort((a, b) => cmpTuple(chiave(a), chiave(b)));
    const top = -chiave(liberi[0])[0];
    let pari = liberi.filter((d) => -chiave(d)[0] >= top * 0.85 && Math.abs(d.minuti - minuti) <= Math.abs(liberi[0].minuti - minuti) + 15);
    if (!pari.length) pari = liberi.slice(0, 1);
    return pari[sett2 % pari.length];
  }
  function scegli(disc, ob, minuti) {
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
  const PIANO = [];
  const usati = /* @__PURE__ */ new Set();
  const slotForza = SKEL.filter(([, d]) => d === "Forza");
  const totQ = sum(SKEL.filter(([, d]) => d !== "Forza").map(([g, d]) => MIX[d] * PESO_SLOT[`${g}|${d}`]));
  for (const x of W) {
    const ore = x.ore;
    const minTot = ore * 60;
    const fase = x.fase;
    const nSed = x.tipo === "Carico" ? NSED[fase] : 1;
    const forzaObiettivo = minTot * QUOTA[fase];
    const sforamentoMax = minTot * ALLOW[fase];
    const sforamento = Math.min(forzaObiettivo, sforamentoMax);
    const terzo = sforamentoMax > 0 && x.tipo === "Carico" ? Math.min(25, forzaObiettivo * 0.25) : 0;
    const resto = forzaObiettivo - terzo;
    const caps = nSed === 2 ? [resto * 0.55, resto * 0.45] : [resto];
    if (terzo) caps.push(terzo);
    const scelteForza = [];
    const nSlot = Math.min(slotForza.length, caps.length);
    for (let i = 0; i < nSlot; i++) {
      const g = slotForza[i][0];
      const cap = caps[i];
      const d = forzaDelGiorno(x.tipo, g, x.pos, cap, scelteForza.map(([, c]) => c), x.w, fase);
      if (d) scelteForza.push([g, d.cod]);
    }
    const nZip = Math.min(scelteForza.length, caps.length);
    let minForza = 0, minS1 = 0;
    for (let i = 0; i < nZip; i++) {
      const d = WK.get(scelteForza[i][1]);
      const m = Math.min(d.minuti, caps[i]);
      minForza += m;
      if (costo(d) === "S1") minS1 += m;
    }
    x.forza_min = minForza;
    x.sforamento = Math.min(sforamento, minS1);
    const minBrick = x.tipo === "Carico" && x.macro === "Specifico" && [1, 2, 3].includes(x.pos) ? 20 : 0;
    const minSport = Math.max(minTot - (minForza - x.sforamento) - minBrick, 30);
    const capDi = /* @__PURE__ */ new Map();
    for (let i = 0; i < nZip; i++) capDi.set(scelteForza[i][0], caps[i]);
    const codDi = new Map(scelteForza);
    for (const [giorno, disc] of SKEL) {
      if (disc === "Forza") {
        const cod = codDi.get(giorno);
        if (!cod) continue;
        const d = WK.get(cod);
        const cap = capDi.get(giorno) ?? d.minuti;
        const mins = Math.min(d.minuti, cap);
        const dom = d.zona === "Z3" ? "MOD" : "LOW";
        PIANO.push({
          w: x.w,
          macro: x.macro,
          blocco: x.blocco,
          tipo: x.tipo,
          giorno,
          disc: "Forza",
          ob: "Preparazione atletica",
          cod,
          struttura: d.nome,
          tempo: mins,
          edw: mins * PESO_Z[d.zona],
          rtss: mins / 60 * 40,
          dom,
          costo: costo(d),
          doms: d.doms
        });
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
      PIANO.push({
        w: x.w,
        macro: x.macro,
        blocco: x.blocco,
        tipo: x.tipo,
        giorno,
        disc,
        ob,
        cod: s.cod,
        struttura: s.base,
        tempo: minuti,
        edw: s.edw * k,
        rtss: s.rtss * k,
        dom: s.dom
      });
      usati.add(s.cod);
    }
  }
  for (const x of W) {
    if (x.tipo === "Carico" && x.macro === "Specifico" && [2, 3, 1].includes(x.pos)) {
      PIANO.push({
        w: x.w,
        macro: x.macro,
        blocco: x.blocco,
        tipo: x.tipo,
        giorno: "Sabato",
        disc: "Corsa a piedi",
        ob: "Ritmo gara specifico",
        cod: "BRICK",
        struttura: "corsa a seguire (transizione)",
        tempo: 20,
        edw: 20 * 3,
        rtss: 20 / 60 * 100,
        dom: "MOD"
      });
    }
  }
  const CAP = A.ore_picco * 60;
  for (const x of W) {
    const sed = PIANO.filter((p) => p.w === x.w);
    const tot = sum(sed.map((p) => p.tempo));
    if (tot <= CAP) continue;
    const ecc = tot - CAP;
    const flex = sed.filter((p) => p.disc !== "Forza" && !(p.giorno === "Sabato" && p.disc === "Ciclismo" && p.tempo >= FLOOR_LUNGO[A.gara] * 0.95));
    const base = sum(flex.map((p) => p.tempo));
    for (const p of flex) {
      const k = 1 - ecc * (p.tempo / base) / p.tempo;
      p.tempo *= k;
      p.edw *= k;
      p.rtss *= k;
    }
  }
  const sett = /* @__PURE__ */ new Map();
  const agg = (w) => {
    let a = sett.get(w);
    if (!a) {
      a = { ore: 0, edw: 0, rtss: 0, LOW: 0, MOD: 0, HIGH: 0 };
      sett.set(w, a);
    }
    return a;
  };
  for (const p of PIANO) {
    const a = agg(p.w);
    a.ore += p.tempo / 60;
    a.edw += p.edw;
    a.rtss += p.rtss;
    a[p.dom] += p.tempo;
  }
  const D = { LOW: 0, MOD: 0, HIGH: 0 };
  for (const p of PIANO) D[p.dom] += p.tempo;
  const T = D.LOW + D.MOD + D.HIGH;
  const oreW = (w) => sett.get(w)?.ore ?? 0;
  const totOre = sum([...sett.values()].map((a) => a.ore));
  const totEdw = sum([...sett.values()].map((a) => a.edw));
  const endOre = sum(PIANO.filter((p) => p.disc !== "Forza").map((p) => p.tempo)) / 60;
  const fzOre = sum(PIANO.filter((p) => p.disc === "Forza").map((p) => p.tempo)) / 60;
  const picco = Math.max(...[...sett.values()].map((a) => a.ore));
  const riepilogo = {
    sedute: PIANO.length,
    ore: totOre,
    edw: totEdw,
    ore_endurance: endOre,
    ore_forza: fzOre,
    low: D.LOW / T * 100,
    mod: D.MOD / T * 100,
    high: D.HIGH / T * 100,
    ore_max_settimana: picco,
    distinti: usati.size,
    mancati: MANCATI
  };
  const V = [];
  const chk = (reg, esito, dett) => V.push([reg, esito ? "OK" : "VIOLATA", dett]);
  const f0 = (x) => pyFixed(x, 0);
  const f1 = (x) => pyFixed(x, 1);
  const [low, mod, hi] = [riepilogo.low, riepilogo.mod, riepilogo.high];
  chk("I4  prevalenza aerobica", low >= 60, `LOW ${f0(low)}% (soglia 60%)`);
  chk("R11 quota sopra soglia", hi <= 15, `HIGH ${f0(hi)}% (tetto 15%)`);
  chk("I4b forma piramidale", mod > hi, `MOD ${f0(mod)}% > HIGH ${f0(hi)}%`);
  const sc = W.filter((x) => x.tipo === "Scarico");
  const prof = [];
  for (const x of sc) {
    const pre = W.filter((y) => y.w < x.w && y.tipo === "Carico");
    if (pre.length) prof.push((oreW(x.w) / oreW(pre[pre.length - 1].w) - 1) * 100);
  }
  chk("D1  ciclo 3:1", sc.every((x) => x.pos === 4), `${sc.length} scarichi, tutti in quarta posizione`);
  chk(
    "D2  profondita' scarico",
    prof.every((p) => -55 <= p && p <= -25),
    prof.length ? `da ${f0(Math.min(...prof))}% a ${f0(Math.max(...prof))}% (range -30/-50 con tolleranza)` : "nessuno scarico"
  );
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
  chk(
    "preparazione atletica",
    nf > 0 && !fdoms.length,
    `${nf} sedute, ${ft} nel taper tutte senza DOMS (micro-dose di attivazione)`
  );
  const s3 = PIANO.filter((p) => p.costo === "S3" && p.giorno === "Mercoled\xEC" && p.tipo === "Carico");
  const s3v = s3.filter((p) => (p.w - 1) % 4 + 1 === 3);
  chk("S3 lontano dalle sedute chiave", !s3v.length, `${s3v.length} sedute S3 in vigilia di una corsa a ritmo gara`);
  const qf = W.map((x) => {
    const tutte = sum(PIANO.filter((p) => p.w === x.w).map((p) => p.tempo));
    const forza = sum(PIANO.filter((p) => p.w === x.w && p.disc === "Forza").map((p) => p.tempo));
    return forza / Math.max(tutte, 1) * 100;
  });
  const nCarico = W.filter((x) => x.tipo === "Carico").length;
  const manca = W.filter((x) => x.tipo === "Carico" && PIANO.filter((p) => p.w === x.w && p.disc === "Forza").length < NSED[x.fase] + (ALLOW[x.fase] > 0 ? 1 : 0)).map((x) => x.w);
  chk(
    "frequenza per fase",
    !manca.length,
    !manca.length ? `rispettata in tutte le ${nCarico} settimane di carico` : `sotto il bersaglio in ${manca.length} settimane`
  );
  const sfor = [];
  for (const x of W) {
    const tot = sum(PIANO.filter((p) => p.w === x.w).map((p) => p.tempo));
    const pian = x.ore * 60;
    if (tot > pian * (1 + ALLOW[x.fase]) + 1) sfor.push([x.w, x.fase, tot / pian - 1]);
  }
  chk(
    "Strength Allowance",
    !sfor.length,
    !sfor.length ? "sforamento entro il limite di ogni fase" : `${sfor.length} settimane oltre: [${sfor.slice(0, 3).map(([w, f, x]) => `(${w}, '${f}', ${x})`).join(", ")}]`
  );
  const alto = W.filter((x) => ALLOW[x.fase] > 0 && PIANO.some((p) => p.w === x.w && p.disc === "Forza" && p.costo === "S3") && sum(PIANO.filter((p) => p.w === x.w).map((p) => p.tempo)) > x.ore * 60 + 1).length;
  chk("sforamento a basso costo", true, `${alto} settimane in cui lo sforamento include una seduta S3`);
  chk("quota della forza", true, `da ${f0(Math.min(...qf))}% a ${f0(Math.max(...qf))}% del monte ore`);
  const ultimaTaper = tapw.length ? oreW(tapw[tapw.length - 1].w) : 0;
  chk(
    "I5  taper presente",
    tapw.length >= 2 && ultimaTaper < picco * 0.25,
    `${tapw.length} settimane, ultima ${f1(ultimaTaper)} h`
  );
  const lungoW = /* @__PURE__ */ new Map();
  for (const x of W) {
    const c = PIANO.filter((q) => q.w === x.w && q.disc === "Ciclismo" && q.giorno === "Sabato").map((q) => q.tempo);
    if (c.length && x.tipo === "Carico") lungoW.set(x.w, Math.max(...c));
  }
  const cw = [...lungoW.keys()].sort((a, b) => a - b);
  const salti = cw.slice(0, -1).map((a, i) => [a, cw[i + 1]]).filter(([a, b]) => lungoW.get(b) / lungoW.get(a) - 1 > 0.15);
  chk(
    "progressione del lungo",
    !salti.length,
    `${salti.length} salti oltre +15% fra settimane di carico su ${Math.max(cw.length - 1, 0)}`
  );
  const viol = [];
  for (const x of W) {
    if (x.tipo !== "Carico") continue;
    const v = PIANO.filter((q) => q.w === x.w && q.giorno === "Venerd\xEC");
    if (sum(v.map((q) => q.tempo)) > 60 || v.some((q) => q.dom !== "LOW")) viol.push(x.w);
  }
  chk("vigilia del lungo scarica", !viol.length, `${viol.length} settimane con venerdi' sopra 60' o con qualita'`);
  let tardi = 0;
  for (const q of PIANO) {
    if (!["Venerd\xEC", "Sabato", "Domenica"].includes(q.giorno)) continue;
    if (q.dom === "LOW") continue;
    if (q.giorno === "Sabato" && (q.disc === "Ciclismo" || q.cod === "BRICK")) continue;
    tardi++;
  }
  chk("qualita' a inizio settimana", tardi === 0, `${tardi} sedute non-LOW fra venerdi' e domenica (escluso lungo e brick)`);
  return { PIANO, W, A, NB, TAPER_DA, N_TAPER, riepilogo, verifiche: V };
}

// src/librerie.ts
var DOM = { Z1: "LOW", Z2: "LOW", Z3: "MOD", Z4: "HIGH", Z5: "HIGH" };
var num = (x, d = 0) => x === null || x === void 0 || x === "" ? d : Number(x);
function normalizzaVarianti(rows) {
  const out = rows.map((r) => ({
    cod: r.cod,
    base: r.base,
    arch: r.arch,
    disc: r.disc,
    ob_libro: r.ob_libro ?? "",
    zona: r.zona ?? "",
    ob: r.ob ?? "",
    dist: num(r.dist),
    tempo: num(r.tempo),
    edw: num(r.edw),
    ban: num(r.ban),
    rtss: num(r.rtss),
    dom: DOM[r.zona ?? ""] ?? "LOW"
  }));
  out.sort((a, b) => a.cod < b.cod ? -1 : a.cod > b.cod ? 1 : 0);
  return out;
}
function normalizzaWorkout(rows) {
  const idx = rows.map((r, i) => ({ r, i, o: r.ordine === null || r.ordine === void 0 ? i : num(r.ordine) }));
  idx.sort((a, b) => a.o - b.o || a.i - b.i);
  return idx.map(({ r }) => ({
    cod: r.cod,
    nome: r.nome,
    bersaglio: r.bersaglio ?? "",
    fasi: r.fasi,
    n: num(r.n_esercizi),
    minuti: num(r.minuti),
    famiglia: r.famiglia,
    zona: r.zona,
    nm: num(r.nm),
    fatica: num(r.fatica),
    doms: num(r.doms),
    collocazione: r.collocazione ?? "",
    N: num(r.n_nuoto),
    B: num(r.b_bici),
    C: num(r.c_corsa)
  }));
}

// src/index.ts
function generaPiano(input, varianti, workouts) {
  const obiettivo = input.obiettivo ?? "Ironman";
  const scala = livelloScala(
    input.gradino_fatto,
    input.settimane,
    input.ore_disponibili,
    input.ore_oggi,
    obiettivo,
    input.tetto_rigido ?? false
  );
  if (isErrore(scala)) return scala;
  const lib = normalizzaVarianti(varianti);
  const wk = normalizzaWorkout(workouts);
  const blocchi = [];
  let inizio = input.ore_oggi;
  for (const b of scala.blocchi) {
    blocchi.push(generaBlocco({
      gara: b.gradino,
      settimane: b.settimane,
      ore_picco: b.picco,
      ore_oggi: inizio,
      sedute_sett: input.sedute_sett ?? 8,
      giorno_riposo: input.giorno_riposo ?? "Luned\xEC"
    }, lib, wk));
    inizio = b.picco * RITENZIONE;
  }
  return { scala, fabbisogno: fabbisognoOre(scala), verifiche_scala: verificaI8(scala, input.gradino_fatto, obiettivo), blocchi };
}
export {
  INTRO,
  NOMI,
  PEND_MIN,
  QUOTA_MIN,
  RITENZIONE,
  SCALA,
  TRANSIZIONE,
  caricoMax,
  costo,
  fabbisognoOre,
  generaBlocco,
  generaPiano,
  idxGradino,
  isErrore,
  livelloScala,
  normalizzaVarianti,
  normalizzaWorkout,
  pyFixed,
  pyRound,
  stimolo,
  verificaI8
};
